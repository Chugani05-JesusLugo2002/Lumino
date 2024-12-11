from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from accounts.forms import LoginForm, SignupForm


def user_login(request: HttpRequest) -> HttpResponse:
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username, password = form.get_credentials()
        if user := authenticate(request, username=username, password=password):
            login(request, user)
            return redirect('subjects:subject-list')
    return render(request, 'accounts/login.html', dict(form=form))


def user_logout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('home')


def user_signup(request: HttpRequest) -> HttpResponse:
    form = SignupForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('subjects:subject-list')
    return render(request, 'accounts/signup.html', dict(form=form))
