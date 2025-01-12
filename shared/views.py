from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.utils import translation


def index(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('subjects:subject-list')
    return render(request, 'index.html')

def setlang(request, langcode):
    next = request.GET.get('next', '/')
    translation.activate(langcode)
    response = redirect(next)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, langcode)
    return response



