from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import SignUpForm, LogInForm


def index(request):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        sign_up_form = SignUpForm

        render(request, 'index.html', {
            'sign_up_form': sign_up_form
        })


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            form.save()

            user = authenticate(username=login, password=password)
            login(request, user)

            return redirect('index')



def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST):
        if form.is_valid():
            login = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')

            user = authenticate(username=login, password=password)
            login(request, user)

            return redirect('index')


def log_out(request):
    logout(request)
    
    return redirect('index')
