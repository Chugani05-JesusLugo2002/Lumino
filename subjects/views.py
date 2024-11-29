from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render


def subject_list(request: HttpRequest) -> HttpResponse:
    subjects = request.user.profile.get_subject_list()
    return render(request, 'subjects/subject-list.html', dict(subjects=subjects))


def subject_detail(request: HttpRequest) -> HttpResponse:
    pass


def subject_lessons(request: HttpRequest) -> HttpResponse:
    pass


def lesson_detail(request: HttpRequest) -> HttpResponse:
    pass


def add_lesson(request: HttpRequest) -> HttpResponse | HttpResponseForbidden:
    pass


def edit_lesson(request: HttpRequest) -> HttpResponse | HttpResponseForbidden:
    pass


def delete_lesson(request: HttpRequest) -> HttpResponse | HttpResponseForbidden:
    pass


def mark_list(request: HttpRequest) -> HttpResponse | HttpResponseForbidden:
    pass


def edit_marks(request: HttpRequest) -> HttpResponse | HttpResponseForbidden:
    pass
