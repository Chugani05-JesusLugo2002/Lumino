from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render

from shared.utils import assert_role
from .models import Profile
from .forms import EditProfileForm


@login_required
def user_detail(request: HttpRequest, username: str) -> HttpResponse:
    target_user = User.objects.get(username=username)
    return render(request, 'users/user_detail.html', dict(target_user=target_user))


@login_required
def edit_profile(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        if (form := EditProfileForm(request.POST, request.FILES, instance=request.user.profile)).is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.add_message(request, messages.SUCCESS, 'User profile has been successfully saved.')
            return redirect('user-detail', profile.user)
    else:
        form = EditProfileForm(instance=request.user.profile)
    return render(request, 'users/edit_profile.html', dict(form=form, messages=messages.get_messages(request)))

@login_required
@assert_role(Profile.Role.STUDENT)
def leave(request: HttpRequest) -> HttpResponse | HttpResponseForbidden:
    request.user.delete()
    messages.add_message(request, messages.SUCCESS, 'Good bye! Hope to see you soon.')
    return redirect('home')
