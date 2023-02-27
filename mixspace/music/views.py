from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .models import CustomAbstractUser as User, Follow, Track, Like
from .forms import SignUpForm, LogInForm, AddSetForm, UserAvatarForm
from .tokens import account_activation_token

from datetime import datetime
from itertools import chain


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        messages.success(request, '<h3 class="email-conf">Email confirmation.</h3></br> \
        <ul class="errorlist"><li>Thank you for \
        your email confirmation. now you can login to your account.</li></ul>')
    else:
        messages.error(request, '<h3 class="email-conf">Email confirmation.</h3></br> \
        <ul class="errorlist"><li>Activation link is \
        invalid.</li></ul>')
    
    return redirect('log_in')


def activate_email(request, user, email):
    mail_subject = 'Activate mix-space\'s user account.'
    message = render_to_string('music/messages/activate_mess.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'Protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[email])
    if email.send():
        messages.success(request, f'<h3 class="email-conf">Email confirmation.</h3></br> \
        <ul class="errorlist"><li>Dear \
        <b>{user}</b>, please go to your email <b>{email}</b> inbox and  \
        click on received activation link to confirm and complete the \
        registration. <b>Note:</b> Check your spam folder.</li></ul>')
    else:
        messages.error(request, f'<h3 class="email-conf">Email confirmation.</h3></br> \
        <ul class="errorlist"><li>Problem sending \
        email to {email}, check if you typed it correctly.</ul>/<li>')


def index(request):
    all_tracks = Track.objects.all().order_by('-time_added')
    paginator = Paginator(all_tracks, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'music/index.html', {
        'page_obj': page_obj
    })


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():            
            user = form.save(commit=False)
            user.is_active = False
            form.save()

            activate_email(request, user, form.cleaned_data.get('email'))
            return redirect('log_in')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            return redirect('sign_up')
    else:
        form = SignUpForm
        return render(request, 'music/sign_up.html', {
            'form': form
        })


def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            login_ = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')

            user = authenticate(email=login_, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, '<ul class="errorlist"><li>Logged in \
                successfully.</li></ul>')
                return redirect('index')
            else:
                messages.error(request, '<ul class="errorlist"><li>Invalid \
                login and/or password.</li></ul>')
                return redirect('log_in')
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, '<ul class="errorlist"><li>You must \
                    pass the reCAPTCHA.</li></ul>')
                    continue
                messages.error(request, error)
            return redirect('log_in')
    else:
        form = LogInForm
        return render(request, 'music/log_in.html', {
            'form': form
        })


@login_required(login_url='/log-in')
def log_out(request):
    logout(request)

    messages.success(request, '<ul class="errorlist"><li>Logged out \
    successfully.</li></ul>')
    return redirect('index')


@login_required(login_url='/log-in')
def upload(request):
    if request.method == 'POST':
        form = AddSetForm(request.POST, request.FILES)
        if form.is_valid():
            new_set = form.save(commit=False)
            new_set.artist = User.objects.get(username=request.user.username)
            new_set.time_added = datetime.now()
            new_set.save()

            return redirect('index')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            return redirect('upload')
    else:
        form = AddSetForm()
        return render(request, 'music/upload.html', {
            'form': form
        })  


def show_user(request, username):
    user = User.objects.get(username=username)
    if request.user.username == username:
        logged_in = True
    else:
        logged_in = False
        
    user_tracks = Track.objects.filter(artist=user).order_by('-time_added')
    paginator = Paginator(user_tracks, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    form = UserAvatarForm()
    
    try:
        avatar = user.avatar.url
    except ValueError:
        avatar = False

    return render(request, 'music/user_profile.html', {
        'username': user.username,
        'avatar': avatar,
        'logged_in': logged_in,
        'page_obj': page_obj,
        'form': form        
    })


def like(request, pk):
    if request.method == 'POST':
        track = Track.objects.get(pk=pk)

        try:
            like_ = Like.objects.get(track=track, user=request.user)
            like_.delete()
        except Like.DoesNotExist:
            like_ = Like(track=track, user=request.user)
            like_.save()
        
        return JsonResponse({'success': 'Follows are updated successfully.'},
                            status=200)
    else:
        try:
            track = Track.objects.get(pk=pk)
        except Track.DoesNotExist:
            return JsonResponse({'error': 'Track not exist.'},
                                status=404)
        likes_count = Like.objects.filter(track=track).count()
        data = {
            'likes_count': likes_count,
        }
        
        return JsonResponse(data)
    

@login_required(login_url='/log-in')
def liked(request):
    likes = Like.objects.filter(user=request.user)
    tracks = Track.objects.filter(like__in=like)
    
    paginator = Paginator(tracks, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'music/liked.html', {
        'page_obj': page_obj
    })
 

@login_required(login_url='/log-in')
def follow(request, username):
    if request.method == 'POST':
        user = User.objects.get(username=username)
        if request.user in user.followed.all():
            user.followed.remove(request.user)
            request.user.following.remove(user)
        else:
            user.followed.add(request.user)
            request.user.following.add(user)
            
        return JsonResponse({'success': 'Follows are updated successfully.'},
        status=200)
    else:
        user = User.objects.get(username=username)
        if request.user in user.followed.all():
            is_followed = True
        elif user is not request.user:
            is_followed = False
        
        data = {
            'is_followed': is_followed,
        }
        
        return JsonResponse(data)
    
 
@login_required(login_url='/log-in')  
def following(request):
    followed_users = list(request.user.following.all())
    tracks = Set.objects.filter(artist__in=followed_users).order_by('-time_added')
    paginator = Paginator(tracks, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'music/following.html', {
        'page_obj': page_obj
    })
    

def player(request, id):
    track = Set.objects.get(id=id)
    return render(request, 'music/player.html', {
        'track': track,
    })


def search(request):
    if request.method == 'POST':
        q = request.POST['search']
        tracks = Set.objects.filter(title__icontains=q).order_by('-title')
        if tracks.count() < 1:
            empty = True
        else:
            empty = False
        paginator = Paginator(tracks, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'music/search.html', {
            'page_obj': page_obj,
            'empty': empty
        })


@login_required(login_url='/log-in')
def avatar_upload(request):
    if request.method == 'POST':
        form = UserAvatarForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(pk=request.user.id)
            user.avatar.delete()
            user.avatar = form.cleaned_data['avatar']
            user.save()
            
            return redirect(request.META['HTTP_REFERER'])
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            return redirect(request.META['HTTP_REFERER'])
        
        
@login_required(login_url='/log-in')
def delete(request, id):
    if request.method == 'POST':
        track = Set.objects.get(pk=id)
        track.delete()
        return JsonResponse({'success': 'Track is deleted successfully.'},
        status=200)
