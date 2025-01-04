from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import AddLessonForm, EditLessonForm, EditMarkForm, EnrollmentForm, EditMarkFormSetHelper
from .models import Enrollment, Lesson, Subject
from .tasks import deliver_certificate
from users.models import Profile
from shared.utils import assert_role, assert_enrollment


@login_required
def subject_list(request: HttpRequest) -> HttpResponse:
    subjects = request.user.profile.get_subjects()
    return render(request, 'subjects/subject/list.html', dict(subjects=subjects))


@login_required
@assert_enrollment
def subject_detail(request: HttpRequest, subject_code: str) -> HttpResponse:
    subject = Subject.objects.get(code=subject_code)
    lessons = subject.lessons.all()
    return render(request, 'subjects/subject/detail.html', dict(subject=subject, lessons=lessons))


@login_required
@assert_enrollment
def lesson_detail(request: HttpRequest, subject_code: str, lesson_pk: int) -> HttpResponse:
    lesson = Lesson.objects.get(pk=lesson_pk)
    subject = lesson.subject
    return render(request, 'subjects/lesson/detail.html', dict(subject=subject, lesson=lesson))

@login_required
@assert_enrollment
@assert_role(Profile.Role.TEACHER)
def add_lesson(request: HttpRequest, subject_code: str) -> HttpResponse | HttpResponseForbidden:
    subject = Subject.objects.get(code=subject_code)
    if request.method == 'POST':
        if (form := AddLessonForm(subject, request.POST)).is_valid():
            messages.add_message(request, messages.SUCCESS, 'Lesson was successfully added.')
            lesson = form.save()
            return redirect(subject)
    else:
        form = AddLessonForm(subject)
    return render(request, 'subjects/lesson/add.html', dict(subject=subject, form=form))


@login_required
@assert_enrollment
def edit_lesson(
    request: HttpRequest, subject_code: str, lesson_pk: int
) -> HttpResponse | HttpResponseForbidden:
    lesson = Lesson.objects.get(pk=lesson_pk)
    subject = lesson.subject
    if request.method == 'POST':
        if (form := EditLessonForm(request.POST, instance=lesson)).is_valid():
            lesson = form.save()
            messages.add_message(request, messages.SUCCESS, 'Changes were successfully saved.')
    form = EditLessonForm(instance=lesson)
    return render(request, 'subjects/lesson/edit.html', dict(subject=subject, form=form))


@login_required
@assert_enrollment
def delete_lesson(
    request: HttpRequest, subject_code: str, lesson_pk: int
) -> HttpResponse | HttpResponseForbidden:
    lesson = Lesson.objects.get(pk=lesson_pk)
    subject = lesson.subject
    lesson.delete()
    messages.add_message(request, messages.SUCCESS, 'Lesson was successfully deleted.')
    return redirect(subject)


@login_required
@assert_enrollment
def mark_list(request: HttpRequest, subject_code: str) -> HttpResponse | HttpResponseForbidden:
    subject = Subject.objects.get(code=subject_code)
    enrolls = subject.enrollments.all()
    return render(request, 'subjects/mark/list.html', dict(subject=subject, enrolls=enrolls))


@login_required
@assert_enrollment
def edit_marks(request: HttpRequest, subject_code: str) -> HttpResponse | HttpResponseForbidden:
    subject = Subject.objects.get(code=subject_code)
    
    MarkFormSet = modelformset_factory(Enrollment, EditMarkForm, extra=0)
    queryset = subject.enrollments.all()
    if request.method == 'POST':
        if (formset := MarkFormSet(queryset=queryset, data=request.POST)).is_valid():
            formset.save()
            messages.add_message(request, messages.SUCCESS, 'Marks were successfully saved.')
            return redirect(reverse('subjects:edit-marks', kwargs={'subject_code': subject_code}))
    else:
        formset = MarkFormSet(queryset=queryset)
    helper = EditMarkFormSetHelper()
    return render(
        request,
        'subjects/mark/edit.html',
        dict(subject=subject, formset=formset, helper=helper),
    )


@login_required
def enroll_subjects(request: HttpRequest) -> HttpResponse | HttpResponseForbidden:
    title = 'Enrollments'
    if request.method == 'POST':
        if (form := EnrollmentForm(request.user, enrolling=True, data=request.POST)).is_valid():
            form.enrolls(request.user)
            messages.add_message(request, messages.SUCCESS, 'Successfully enrolled in the chosen subjects.')
            return redirect('subjects:subject-list')
    else:
        form = EnrollmentForm(request.user)
    return render(request, 'subjects/subject/enrollment.html', dict(form=form, title=title))


@login_required
def unenroll_subjects(request: HttpRequest) -> HttpResponse | HttpResponseForbidden:
    title = 'Unenrollments'
    if request.method == 'POST':
        if (form := EnrollmentForm(request.user, enrolling=False, data=request.POST)).is_valid():
            form.unenrolls(request.user)
            messages.add_message(request, messages.SUCCESS, 'Successfully unenrolled from the chosen subjects.')
            return redirect('subjects:subject-list')
    else:
        form = EnrollmentForm(request.user, enrolling=False)
    return render(request, 'subjects/subject/enrollment.html', dict(form=form, title=title))


@login_required
def request_certificate(request: HttpRequest) -> HttpResponse:
    if request.user.enrollments.filter(mark=None).count() > 0:
        return HttpResponseForbidden()
    deliver_certificate.delay(request.build_absolute_uri(), request.user)
    return render(request, 'subjects/certificate/feedback.html')
