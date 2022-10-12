from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import User, Set
from .forms import SignUpForm, LogInForm, AddSetForm, UserAvatarForm

from datetime import datetime


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

            form.save()

            return JsonResponse({'info': 'Log in will be enabled after email verification.'},
            status=201)

        else:
            return JsonResponse({'error': 'Some of entered data is invalid.'},
            status=400)
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
                return JsonResponse({'error': 'Invalid login and/or password.'},
                status=400)  
        else:
            return JsonResponse({'error': 'Some of entered data is invalid.'},
            status=400)
    else:
        form = LogInForm
        return render(request, 'music/log_in.html', {
            'form': form
        })
    


def log_out(request):
    logout(request)

    return redirect('index')


def upload(request):
    if request.method == 'POST':
        form = AddSetForm(request.POST, request.FILES)
        if form.is_valid():
            new_set = form.save(commit=False)
            new_set.artist = User.objects.get(username=request.user.username)
            new_set.time_added = datetime.now()
            new_set.save()

            return JsonResponse({'info': 'Track is added successfully.'},
            status=201)  
        else:
            return JsonResponse({'error': 'Some of entered data is invalid.'},
            status=400)
    else:
        form = AddSetForm
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

    return render(request, 'music/user_profile.html', {
        'username': user.username,
        'avatar': user.avatar.path,
        'logged_in': logged_in,
        'page_obj': page_obj        
    })


def likes(request, id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            track = Set.objects.get(id=id)
            if User.set_set.filter(pk=id).exists() and request.user is not track.artist:
                track.likes.remove(request.user)
            elif request.user is not track.artist:
                track.likes.add(request.user)
            return JsonResponse({'success': 'Follows are updated successfully.'},
            status=204)
        else:
            return JsonResponse({'error': 'You must be logged in.'},
            status=204)
    else:
        track = Set.objects.get(id=id)
        likes_count = track.likes.count()
        user_liked = False
        if User.set_set.filter(pk=id).exists() and request.user is not track.artist:
            user_liked = True
        
        data = {
            'likes_count': likes_count,
            'user_liked': user_liked
        }
        
        return JsonResponse(data)
 
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
