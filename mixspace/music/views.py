from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import User, Set
from .forms import SignUpForm, LogInForm, AddSetForm, UserAvatarForm

from datetime import datetime
from itertools import chain


def index(request):
    all_tracks = Set.objects.all().order_by('-time_added')
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
            login_ = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            
            user = form.save(commit=False)
            user.is_active = False
            form.save()

            form = LogInForm
            
            return render(request, 'music/log_in.html', {
                'form': form,
                'info': 'Log in will be enabled after email verification. Check your email.'
            })
        else:
            return render(request, 'music/sign_up.html', {
                'form': form
            })
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

            user = authenticate(username=login_, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'music/log_in.html', {
                    'form': form,
                    "info": "Invalid login and/or password.",
                })
        else:
            redirect('log_in')
    else:
        form = LogInForm
        return render(request, 'music/log_in.html', {
            'form': form
        })
    


@login_required(login_url='/log-in')
def log_out(request):
    logout(request)

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
            return render(request, 'music/upload.html', {
                'form': form
        })  
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
        
    user_tracks = Set.objects.filter(artist=user).order_by('-time_added')
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


def like(request, id):
    if request.method == 'POST':
        track = Set.objects.get(id=id)
        if request.user in track.like.all():
            track.like.remove(request.user)
        else:
            track.like.add(request.user)
            
        return JsonResponse({'success': 'Follows are updated successfully.'},
        status=200)
    else:
        track = Set.objects.get(id=id)
        likes_count = track.like.count()
        data = {
            'likes_count': likes_count,
        }
        
        return JsonResponse(data)
    

@login_required(login_url='/log-in')
def liked(request):
    tracks = Set.objects.filter(like=request.user).order_by('-time_added')
    
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
            # user.avatar=request.FILES['avatar']
            user.avatar = form.cleaned_data['avatar']
            user.save()
            
            return redirect(request.META['HTTP_REFERER'])
        else:
            return redirect(request.META['HTTP_REFERER'])
