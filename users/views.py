from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render

from .forms import EditProfileForm


@login_required
def user_detail(request: HttpRequest, username: str) -> HttpResponse:
    consumer = User.objects.get(username=username)
    return render(request, 'users/user_detail.html', dict(consumer=consumer))


@login_required
def edit_profile(request: HttpRequest, username: str) -> HttpResponse:
    user = User.objects.get(username=username)
    user_profile = user.profile
    if request.method == 'POST':
        if (form := EditProfileForm(request.POST, request.FILES, instance=user_profile)).is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('users:user-detail', username)
    else:
        form = EditProfileForm(instance=user_profile)
    return render(request, 'users/edit_profile.html', dict(form=form))


@login_required
def request_certificate(request: HttpRequest) -> HttpResponse:
    pass


@login_required
def leave(request: HttpRequest) -> HttpResponse | HttpResponseForbidden:
    pass
