from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import User, Set
from .forms import SignUpForm, LogInForm, AddSetForm, UserAvatarForm

from datetime import datetime


def index(request):
    sign_up_form = SignUpForm
    log_in_form = LogInForm
    add_set_form = AddSetForm

    tracks = Set.objects.all().order_by('-time_added')
    paginator = Paginator(tracks, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'music/index.html', {
        'sign_up_form': sign_up_form,
        'log_in_form': log_in_form,
        'add_set_form': add_set_form,
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


def show_user(reuqest, username):
    user = User.objects.get(username=username)

    data = {
        'user_data': user.serialize
    }

    return JsonResponse(data)


def show_tracks(request):
    last_added = Set.objects.all().order_by('-id')
    paginator = Paginator(last_added, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        'data': [track.serialize for track in  page.object_list],
        'previous_page': objects.has_previous() and objects.previous_page_number() or None,
        'next_page': objects.has_next() and objects.next_page_number() or None
    }
    return JsonResponse(data)
