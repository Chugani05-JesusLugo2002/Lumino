from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render

from .forms import AddLessonForm, EditLessonForm
from .models import Lesson, Subject


@login_required
def subject_list(request: HttpRequest) -> HttpResponse:
    subjects = request.user.profile.get_subject_list()
    return render(request, 'subjects/subject-list.html', dict(subjects=subjects))


@login_required
def subject_detail(request: HttpRequest, subject_code: str) -> HttpResponse:
    subject = Subject.objects.get(code=subject_code)
    lessons = subject.lessons.all()
    return render(request, 'subjects/subject-detail.html', dict(subject=subject, lessons=lessons))


@login_required
def lesson_detail(request: HttpRequest, subject_code: str, lesson_pk: int) -> HttpResponse:
    lesson = Lesson.objects.get(pk=lesson_pk)
    subject = lesson.subject
    return render(request, 'subjects/lesson-detail.html', dict(subject=subject, lesson=lesson))


@login_required
def add_lesson(request: HttpRequest, subject_code: str) -> HttpResponse | HttpResponseForbidden:
    subject = Subject.objects.get(code=subject_code)
    if request.method == 'POST':
        if (form := AddLessonForm(subject, request.POST)).is_valid():
            lesson = form.save()
            return redirect(lesson)
    else:
        form = AddLessonForm(subject)
    return render(request, 'subjects/add-lesson.html', dict(subject=subject, form=form))


@login_required
def edit_lesson(
    request: HttpRequest, subject_code: str, lesson_pk: int
) -> HttpResponse | HttpResponseForbidden:
    lesson = Lesson.objects.get(pk=lesson_pk)
    subject = lesson.subject
    if request.method == 'POST':
        if (form := EditLessonForm(request.POST, instance=lesson)).is_valid():
            lesson = form.save()
            return redirect(lesson)
    else:
        form = EditLessonForm(instance=lesson)
    return render(request, 'subjects/edit-lesson.html', dict(subject=subject, form=form))


@login_required
def delete_lesson(request: HttpRequest) -> HttpResponse | HttpResponseForbidden:
    # TODO: Implements as Bootstrap Modal! -> Base.html implementation pending
    pass


@login_required
def mark_list(request: HttpRequest, subject_code: str) -> HttpResponse | HttpResponseForbidden:
    subject = Subject.objects.get(code=subject_code)
    enrolls = subject.enrollments.all()
    return render(request, 'subjects/mark-list.html', dict(subject=subject, enrolls=enrolls))


@login_required
def edit_marks(request: HttpRequest, subject_code: str) -> HttpResponse | HttpResponseForbidden:
    subject = Subject.objects.get(code=subject_code)
    enrolls = subject.enrollments.all()
    if request.method == 'POST':
        # TODO: Save new marks on database (Ask Sergio)
        return redirect('subjects:mark-list', subject_code=subject.code)
    return render(request, 'subjects/edit-marks.html', dict(subject=subject, enrolls=enrolls))


@login_required
def enroll_subjects(request: HttpRequest) -> HttpResponse | HttpResponseForbidden:
    pass


@login_required
def unenroll_subjects(request: HttpRequest) -> HttpResponse | HttpResponseForbidden:
    pass
