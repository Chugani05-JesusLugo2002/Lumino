from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render

from .models import Lesson, Subject


def subject_list(request: HttpRequest) -> HttpResponse:
    subjects = request.user.profile.get_subject_list()
    return render(request, 'subjects/subject-list.html', dict(subjects=subjects))


def subject_detail(request: HttpRequest, subject_code: str) -> HttpResponse:
    subject = Subject.objects.get(code=subject_code)
    return render(request, 'subjects/subject-detail.html', dict(subject=subject))


def subject_lessons(request: HttpRequest, subject_code: str) -> HttpResponse:
    subject = Subject.objects.get(code=subject_code)
    lessons = subject.lessons.all()
    return render(request, 'subjects/subject-lessons.html', dict(subject=subject, lessons=lessons))


def lesson_detail(request: HttpRequest, subject_code: str, lesson_pk: int) -> HttpResponse:
    lesson = Lesson.objects.get(pk=lesson_pk)
    return render(request, 'subjects/lesson-detail.html', dict(lesson=lesson))


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
