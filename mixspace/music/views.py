from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

from .forms import SignUpForm, LogInForm, AddSetForm, UserAvatarForm


def index(request):
    sign_up_form = SignUpForm
    log_in_form = LogInForm
    add_set_form = AddSetForm

    render(request, 'index.html', {
        'sign_up_form': sign_up_form,
        'log_in_form': log_in_form,
        'add_set_form': add_set_form
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
        else:
            return JsonResponse({'error': 'Some of entered data is invalid.'},
            status=400)



def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')

            user = authenticate(username=login, password=password)
            login(request, user)

            return redirect('index')
        else:
            return JsonResponse({'error': 'Some of entered data is invalid.'},
            status=400)       


def log_out(request):
    logout(request)

    return redirect('index')


def show_user(reuqest, username):
    user = User.objects.get(username=username)

    return render(request, "music/show_profile.html", {
        "profile_owner": user
    })


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
