from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from accounts.forms import LoginForm, SignupForm
from users.models import Profile


def user_login(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        if (form := LoginForm(request.POST)).is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if user := authenticate(request, username=username, password=password):
                login(request, user)
                # return redirect('subjects:subject-list')
                return HttpResponse('logueado')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', dict(form=form))


def user_logout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return render(request, 'accounts/logout.html')


def user_signup(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        if (form := SignupForm(request.POST)).is_valid():
            user = form.save()
            new_profile = Profile(user=user)
            new_profile.save()
            login(request, user)
            # return redirect('subjects:subject-list')
            return HttpResponse('perfil creado')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', dict(form=form))
