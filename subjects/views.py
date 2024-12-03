from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render

from .forms import AddLessonForm
from .models import Lesson, Subject


@login_required
def subject_list(request: HttpRequest) -> HttpResponse:
    subjects = request.user.profile.get_subject_list()
    return render(request, 'subjects/subject-list.html', dict(subjects=subjects))


@login_required
def subject_detail(request: HttpRequest, subject_code: str) -> HttpResponse:
    subject = Subject.objects.get(code=subject_code)
    return render(request, 'subjects/subject-detail.html', dict(subject=subject))


@login_required
def subject_lessons(request: HttpRequest, subject_code: str) -> HttpResponse:
    subject = Subject.objects.get(code=subject_code)
    lessons = subject.lessons.all()
    return render(request, 'subjects/subject-lessons.html', dict(subject=subject, lessons=lessons))


@login_required
def lesson_detail(request: HttpRequest, subject_code: str, lesson_pk: int) -> HttpResponse:
    lesson = Lesson.objects.get(pk=lesson_pk)
    return render(request, 'subjects/lesson-detail.html', dict(lesson=lesson))


@login_required
def add_lesson(request: HttpRequest, subject_code: str) -> HttpResponse | HttpResponseForbidden:
    subject = Subject.objects.get(code=subject_code)
    if request.method == 'POST':
        if (form := AddLessonForm(subject, request.POST)).is_valid():
            lesson = form.save()
            return redirect(lesson)
    else:
        form = AddLessonForm(subject)
    return render(request, 'subjects/add-lesson.html', dict(form=form))


@login_required
def edit_lesson(request: HttpRequest) -> HttpResponse | HttpResponseForbidden:
    pass


@login_required
def delete_lesson(request: HttpRequest) -> HttpResponse | HttpResponseForbidden:
    pass


@login_required
def mark_list(request: HttpRequest) -> HttpResponse | HttpResponseForbidden:
    pass


@login_required
def edit_marks(request: HttpRequest) -> HttpResponse | HttpResponseForbidden:
    pass
