import os

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
from .convert_audio import convert_to_mp3



def index(request):
    if request.method == 'GET':
        all_tracks = Track.objects.all().order_by('-time_added')
        paginator = Paginator(all_tracks, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'index.html', {
            'page_obj': page_obj
        })
    else:
        return render(request, '501.html', status=501)


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            if 'EMAIL' in os.environ and os.getenv('EMAIL') != '':
                activate_email(request, user, form.cleaned_data.get('email'))
            else:
                messages.error(request, f'<h3 class="email-conf">Email confirmation.'
                                        f'</h3></br><ul class="errorlist"><li>Dear <b'
                                        f'>{user}</b>,<br>due to an unconfigured email'
                                        f' address, you will need to ask the admin to '
                                        f'manually verify that your account is '
                                        f'active.</li></ul>')
            return redirect('log_in')
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, '<ul class="errorlist"><li>You must'
                                            ' pass the reCAPTCHA.</li></ul>')
                else:
                    messages.error(request, error)
            return redirect('sign_up')
    elif request.method == 'GET':
        form = SignUpForm
        return render(request, 'sign_up.html', {
            'form': form
        })
    else:
        return render(request, '501.html', status=501)


def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            login_ = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')

            user = authenticate(email=login_, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, '<ul class="errorlist"><li>Logged in '
                                          'successfully.</li></ul>')
                return redirect('index')
            else:
                messages.error(request, '<ul class="errorlist"><li>Invalid '
                                        'login and/or password.</li></ul>')
                return redirect('log_in')
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, '<ul class="errorlist"><li>You must'
                                            ' pass the reCAPTCHA.</li></ul>')
                else:
                    messages.error(request, error)
            return redirect('log_in')
    elif request.method == 'GET':
        form = LogInForm
        return render(request, 'log_in.html', {
            'form': form
        })
    else:
        return render(request, '501.html', status=501)


@login_required(login_url='/log-in')
def log_out(request):
    if request.method == 'GET':
        logout(request)

        messages.success(request, '<ul class="errorlist"><li>Logged out '
                                  'successfully.</li></ul>')
        return redirect('index')
    else:
        return render(request, '501.html', status=501)


@login_required(login_url='/log-in')
def upload(request):
    if request.method == 'POST':
        form = AddSetForm(request.POST, request.FILES)
        if form.is_valid():
            new_set = form.save(commit=False)
            new_set.artist = request.user
            new_set.file = convert_to_mp3(request.FILES.get('file'))

            new_set.save()

            return redirect('index')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            return redirect('upload')
    elif request.method == 'GET':
        form = AddSetForm()
        return render(request, 'upload.html', {
            'form': form
        })
    else:
        return render(request, '501.html', status=501)


def show_user(request, username):
    if request.method == 'GET':
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
            avatar = None

        return render(request, 'user_profile.html', {
            'username': user.username,
            'avatar': avatar,
            'logged_in': logged_in,
            'page_obj': page_obj,
            'form': form
        })
    else:
        return render(request, '501.html', status=501)


def like(request, pk):
    if request.method == 'POST':
        track = Track.objects.get(pk=pk)

        try:
            like_ = Like.objects.get(track=track, user=request.user)
            like_.delete()
        except Like.DoesNotExist:
            like_ = Like(track=track, user=request.user)
            like_.save()

        return JsonResponse(
            {'success': 'Likes are updated successfully.'},
            status=200
        )
    elif request.method == 'GET':
        try:
            track = Track.objects.get(pk=pk)
        except Track.DoesNotExist:
            return render(request, '404.html', status=404)
        likes_count = Like.objects.filter(track=track).count()

        try:
            Like.objects.get(track=track, user=request.user)
            is_liked = True
        except Like.DoesNotExist:
            is_liked = False

        data = {
            'likes_count': likes_count,
            'is_liked': is_liked
        }

        return JsonResponse(data)
    else:
        return render(request, '501.html', status=501)


@login_required(login_url='/log-in')
def liked(request):
    if request.method == 'GET':
        likes = Like.objects.filter(user=request.user)
        tracks = Track.objects.filter(id__in=likes.values('track_id')).order_by(
            '-time_added')

        paginator = Paginator(tracks, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'liked.html', {
            'page_obj': page_obj
        })
    else:
        return render(request, '501.html', status=501)


@login_required(login_url='/log-in')
def follow(request, username):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, '404.html', status=404)
        try:
            follow_ = Follow.objects.get(user=user, follower=request.user)
            follow_.delete()
        except Follow.DoesNotExist:
            follow_ = Follow(user=user, follower=request.user)
            follow_.save()

        return JsonResponse(
            {'success': 'Follows are updated successfully.'},
            status=200
        )
    elif request.method == 'GET':
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, '404.html', status=404)
        try:
            Follow.objects.get(
                user=user,
                follower=request.user
            )
            is_followed = True
        except Follow.DoesNotExist:
            is_followed = False

        data = {
            'is_followed': is_followed,
        }

        return JsonResponse(data)
    else:
        return render(request, '501.html', status=501)


@login_required(login_url='/log-in')
def following(request):
    if request.method == 'GET':
        follows = Follow.objects.filter(follower=request.user)
        users = User.objects.filter(id__in=follows.values('user_id'))
        tracks = Track.objects.filter(
            artist_id__in=users.values('id')
        ).order_by('-time_added')

        paginator = Paginator(tracks, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'following.html', {
            'page_obj': page_obj
        })
    else:
        return render(request, '501.html', status=501)


def player(request, pk):
    if request.method == 'GET':
        try:
            track = Track.objects.get(pk=pk)
        except Track.DoesNotExist:
            return render(request, '404.html', status=404)

        return render(request, 'player.html', {
            'track': track,
        })
    else:
        return render(request, '501.html', status=501)


def search(request):
    if request.method == 'POST':
        q = request.POST['search']
        tracks = Track.objects.filter(title__icontains=q).order_by('-title')
        if tracks.count() < 1:
            empty = True
        else:
            empty = False
        paginator = Paginator(tracks, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'search.html', {
            'page_obj': page_obj,
            'empty': empty
        })
    elif request.method == 'GET':
        return render(request, '405.html', status=405)
    else:
        return render(request, '501.html', status=501)


@login_required(login_url='/log-in')
def avatar_upload(request):
    if request.method == 'POST':
        form = UserAvatarForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(pk=request.user.id)
            if user.avatar is not None:
                user.avatar.delete()
            user.avatar = request.FILES['avatar']
            user.save()

            return redirect(request.META.get('HTTP_REFERER', 'index'))
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            return redirect(request.META.get('HTTP_REFERER', 'index'))
    elif request.method == 'GET':
        return render(request, '405.html', status=405)
    else:
        return render(request, '501.html', status=501)


@login_required(login_url='/log-in')
def delete(request, pk):
    if request.method == 'POST':
        try:
            track = Track.objects.get(pk=pk)
            if track.artist == request.user:
                track.delete()
            else:
                return render(request, '401.html', status=401)
        except Track.DoesNotExist:
            return render(request, '405.html', status=404)

        return JsonResponse({'success': 'Track is deleted successfully.'},
                            status=200)
    elif request.method == 'GET':
        return render(request, '405.html', status=405)
    else:
        return render(request, '501.html', status=501)


def activate(request, uidb64, token):
    if request.method == 'GET':
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            user = None

        if user is not None and account_activation_token.check_token(user,
                                                                     token):
            user.is_active = True
            user.save()

            messages.success(request,
                             '<h3 class="email-conf">Email confirmation.'
                             '</h3></br><ul class="errorlist"><li>Thank '
                             'you for your email confirmation. now you can'
                             ' login to your account.</li></ul>')
        else:
            messages.error(request, '<h3 class="email-conf">Email confirmation.'
                                    '</h3></br><ul class="errorlist"><li>Activation'
                                    ' link is invalid.</li></ul>')

        return redirect('log_in')
    else:
        return render(request, '501.html', status=501)


def activate_email(request, user, email):
    if request.method == 'GET':
        mail_subject = 'Activate mix-space\'s user account.'
        message = render_to_string('messages/activate_mess.html', {
            'user': user.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'Protocol': 'https' if request.is_secure() else 'http'
        })
        email = EmailMessage(mail_subject, message, to=[email])
        if email.send():
            messages.success(request,
                             f'<h3 class="email-conf">Email confirmation.'
                             f'</h3></br><ul class="errorlist"><li>Dear <b'
                             f'>{user}</b>, please go to your email <b>'
                             f'{email}</b> inbox and click on received '
                             f'activation link to confirm and complete the'
                             f' registration. <b>Note:</b> Check your spam'
                             f' folder.</li></ul>')
        else:
            messages.error(request,
                           f'<h3 class="email-conf">Email confirmation.'
                           f'</h3></br><ul class="errorlist"><li>Problem '
                           f'sending email to {email}, check if you typed'
                           f' it correctly.</ul>/<li>')
    else:
        return render(request, '501.html', status=501)
