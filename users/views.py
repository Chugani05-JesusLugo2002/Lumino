from django.http import HttpRequest, HttpResponse, HttpResponseForbidden


def user_detail(request: HttpRequest, username: str) -> HttpResponse:
    pass


def edit_profile(request: HttpRequest) -> HttpResponse:
    pass


def request_certificate(request: HttpRequest) -> HttpResponse:
    pass


def enroll_subjects(request: HttpRequest) -> HttpResponse | HttpResponseForbidden:
    pass


def unenroll_subjects(request: HttpRequest) -> HttpResponse | HttpResponseForbidden:
    pass


def leave(request: HttpRequest) -> HttpResponse | HttpResponseForbidden:
    pass
