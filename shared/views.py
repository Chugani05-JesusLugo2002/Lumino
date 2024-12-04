from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


def index(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('subjects:subject-list')
    else:
        return render(request, 'index.html')
