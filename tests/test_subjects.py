import random
import re
from http import HTTPStatus

import pytest
from model_bakery import baker
from pytest_django.asserts import assertContains, assertNotContains, assertRedirects

from subjects.models import Enrollment

# ==============================================================================
# STUDENTS
# ==============================================================================


@pytest.mark.dependency()
@pytest.mark.django_db
def test_subject_list_for_students(client, student, another_student):
    own_enrollments = baker.make_recipe('tests.enrollment', student=student, _quantity=10)
    another_enrollments = baker.make_recipe(
        'tests.enrollment', student=another_student, _quantity=10
    )
    client.force_login(student)
    response = client.get('/subjects/')
    response_text = response.content.decode()
    for enrollment in own_enrollments:
        assert re.search(rf'\b{enrollment.subject.code}\b', response_text, re.S | re.M)
    for enrollment in another_enrollments:
        assert not re.search(rf'\b{enrollment.subject.code}\b', response_text, re.S | re.M)


@pytest.mark.dependency(depends=['test_subject_list_for_students'])
@pytest.mark.django_db
def test_subject_list_for_student_contains_links_for_subject_details(client, student):
    SUBJECT_DETAIL_URL = '/subjects/{subject_code}/'
    enrollments = baker.make_recipe('tests.enrollment', student=student, _quantity=10)
    client.force_login(student)
    response = client.get('/subjects/')
    for enrollment in enrollments:
        href = f'href="{SUBJECT_DETAIL_URL.format(subject_code=enrollment.subject.code)}"'
        assertContains(response, href)


@pytest.mark.django_db
def test_enroll_link_exists_in_subject_list_for_students(client, teacher):
    client.force_login(teacher)
    response = client.get('/subjects/')
    assertContains(response, 'href="/subjects/enroll/"')


@pytest.mark.django_db
def test_unenroll_link_exists_in_subject_list_for_students(client, student):
    client.force_login(student)
    response = client.get('/subjects/')
    assertContains(response, 'href="/subjects/unenroll/"')


@pytest.mark.django_db
def test_enroll_subjects_display_right_subjects(client, student):
    subjects = baker.make_recipe('tests.subject', _quantity=10)
    enrollments = baker.make_recipe('tests.enrollment', student=student, _quantity=10)
    client.force_login(student)
    response = client.get('/subjects/enroll/')
    response_text = response.content.decode()
    for unenrolled_subject in subjects:
        assert re.search(
            rf'<label.*?\b{unenrolled_subject.code}\b.*?</label>', response_text, re.M | re.S
        )
    for enrollment in enrollments:
        assert not re.search(
            rf'<label.*?\b{enrollment.subject.code}\b.*?</label>', response_text, re.M | re.S
        )


@pytest.mark.django_db
def test_unenroll_subjects_display_right_subjects(client, student):
    subjects = baker.make_recipe('tests.subject', _quantity=10)
    enrollments = baker.make_recipe('tests.enrollment', student=student, _quantity=10)
    client.force_login(student)
    response = client.get('/subjects/unenroll/')
    response_text = response.content.decode()
    for unenrolled_subject in subjects:
        assert not re.search(
            rf'<label.*?\b{unenrolled_subject.code}\b.*?</label>', response_text, re.M | re.S
        )
    for enrollment in enrollments:
        assert re.search(
            rf'<label.*?\b{enrollment.subject.code}\b.*?</label>', response_text, re.M | re.S
        )


@pytest.mark.django_db
def test_enroll_subjects_works(client, student):
    subjects = baker.make_recipe('tests.subject', _quantity=10)
    subject_pks = [s.pk for s in subjects]
    client.force_login(student)
    payload = dict(subjects=subject_pks)
    response = client.post('/subjects/enroll/', payload, follow=True)
    assertContains(response, 'Successfully enrolled in the chosen subjects.')
    assertRedirects(response, '/subjects/')
    assert list(student.enrolled.values_list('pk', flat=True)) == subject_pks


@pytest.mark.django_db
def test_unenroll_subjects_works(client, student):
    enrollments = baker.make_recipe('tests.enrollment', student=student, _quantity=10)
    subject_pks = [e.subject.pk for e in enrollments]
    client.force_login(student)
    payload = dict(subjects=subject_pks)
    response = client.post('/subjects/unenroll/', payload, follow=True)
    assertContains(response, 'Successfully unenrolled from the chosen subjects.')
    assertRedirects(response, '/subjects/')
    assert student.enrolled.count() == 0


@pytest.mark.django_db
def test_lessons_are_displayed_within_subject_detail_for_students(client, student):
    enrollment = baker.make_recipe('tests.enrollment', student=student)
    subject = enrollment.subject
    subject_lessons = baker.make_recipe('tests.lesson', subject=subject, _quantity=10)
    another_lessons = baker.make_recipe('tests.lesson', _quantity=10)
    client.force_login(student)
    response = client.get(f'/subjects/{subject.code}/')
    assert response.status_code == HTTPStatus.OK
    for lesson in subject_lessons:
        assertContains(response, lesson.title)
    for lesson in another_lessons:
        assertNotContains(response, lesson.title)


@pytest.mark.django_db
def test_subject_detail_is_forbidden_for_non_enrolled_students(client, teacher):
    subject = baker.make_recipe('tests.subject')
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/')
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_lesson_links_exist_in_subject_detail_for_students(client, student):
    LESSON_DETAIL_URL = '/subjects/{subject_code}/lessons/{lesson_pk}/'

    enrollment = baker.make_recipe('tests.enrollment', student=student)
    subject = enrollment.subject
    lessons = baker.make_recipe('tests.lesson', subject=subject, _quantity=10)
    client.force_login(student)
    response = client.get(f'/subjects/{subject.code}/')
    assert response.status_code == HTTPStatus.OK
    for lesson in lessons:
        lesson_detail_url = LESSON_DETAIL_URL.format(subject_code=subject.code, lesson_pk=lesson.pk)
        href = f'href="{lesson_detail_url}"'
        assertContains(response, href)


@pytest.mark.django_db
def test_subject_mark_appears_when_set(client, student):
    enrollment = baker.make_recipe('tests.enrollment', student=student)
    enrollment.mark = 9
    enrollment.save()
    subject = enrollment.subject
    client.force_login(student)
    response = client.get(f'/subjects/{subject.code}/')
    assertContains(response, enrollment.mark)


@pytest.mark.django_db
def test_lesson_detail_for_students(client, student):
    enrollment = baker.make_recipe('tests.enrollment', student=student)
    subject = enrollment.subject
    lesson = baker.make_recipe('tests.lesson', subject=subject)
    url = f'/subjects/{subject.code}/lessons/{lesson.pk}/'
    client.force_login(student)
    response = client.get(url)
    assertContains(response, lesson.content)


@pytest.mark.django_db
def test_lesson_detail_is_forbidden_for_non_enrolled_students(client, teacher):
    subject = baker.make_recipe('tests.subject')
    lesson = baker.make_recipe('tests.lesson', subject=subject)
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/lessons/{lesson.pk}/')
    assert response.status_code == HTTPStatus.FORBIDDEN


# ==============================================================================
# TEACHERS
# ==============================================================================


@pytest.mark.dependency()
@pytest.mark.django_db
def test_subject_list_for_teachers(client, teacher, another_teacher):
    own_teaching = baker.make_recipe('tests.subject', teacher=teacher, _quantity=10)
    another_teaching = baker.make_recipe('tests.subject', teacher=another_teacher, _quantity=10)
    client.force_login(teacher)
    response = client.get('/subjects/')
    response_text = response.content.decode()
    for subject in own_teaching:
        assert re.search(rf'\b{subject.code}\b', response_text, re.S | re.M)
    for subject in another_teaching:
        assert not re.search(rf'\b{subject.code}\b', response_text, re.S | re.M)


@pytest.mark.dependency(depends=['test_subject_list_for_teachers'])
@pytest.mark.django_db
def test_subject_list_for_teachers_contains_links_for_subject_details(client, teacher):
    SUBJECT_DETAIL_URL = '/subjects/{subject_code}/'
    teaching = baker.make_recipe('tests.subject', teacher=teacher, _quantity=10)
    client.force_login(teacher)
    response = client.get('/subjects/')
    for subject in teaching:
        href = f'href="{SUBJECT_DETAIL_URL.format(subject_code=subject.code)}"'
        assertContains(response, href)


@pytest.mark.django_db
def test_lessons_are_displayed_within_subject_detail_for_teachers(client, teacher):
    subject = baker.make_recipe('tests.subject', teacher=teacher)
    subject_lessons = baker.make_recipe('tests.lesson', subject=subject, _quantity=10)
    another_lessons = baker.make_recipe('tests.lesson', _quantity=10)
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/')
    assert response.status_code == HTTPStatus.OK
    for lesson in subject_lessons:
        assertContains(response, lesson.title)
    for lesson in another_lessons:
        assertNotContains(response, lesson.title)


@pytest.mark.django_db
def test_add_lesson_link_exists_in_subject_detail_for_teachers(client, teacher):
    subject = baker.make_recipe('tests.subject', teacher=teacher)
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/')
    href = f'href="/subjects/{subject.code}/lessons/add/'
    assertContains(response, href)


@pytest.mark.django_db
def test_edit_marks_link_exists_in_subject_detail_for_teachers(client, teacher):
    subject = baker.make_recipe('tests.subject', teacher=teacher)
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/')
    href = f'href="/subjects/{subject.code}/marks/'
    assertContains(response, href)


@pytest.mark.django_db
def test_subject_detail_is_forbidden_for_non_teaching_teachers(client, teacher):
    subject = baker.make_recipe('tests.subject')
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/')
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_lesson_links_exist_in_subject_detail_for_teachers(client, teacher):
    LESSON_DETAIL_URL = '/subjects/{subject_code}/lessons/{lesson_pk}/'

    subject = baker.make_recipe('tests.subject', teacher=teacher)
    lessons = baker.make_recipe('tests.lesson', subject=subject, _quantity=10)
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/')
    assert response.status_code == HTTPStatus.OK
    for lesson in lessons:
        lesson_detail_url = LESSON_DETAIL_URL.format(subject_code=subject.code, lesson_pk=lesson.pk)
        href = f'href="{lesson_detail_url}"'
        assertContains(response, href)


@pytest.mark.django_db
def test_edit_lesson_links_exist_in_subject_detail_for_teachers(client, teacher):
    EDIT_LESSON_URL = '/subjects/{subject_code}/lessons/{lesson_pk}/edit/'

    subject = baker.make_recipe('tests.subject', teacher=teacher)
    lessons = baker.make_recipe('tests.lesson', subject=subject, _quantity=10)
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/')
    assert response.status_code == HTTPStatus.OK
    for lesson in lessons:
        lesson_detail_url = EDIT_LESSON_URL.format(subject_code=subject.code, lesson_pk=lesson.pk)
        href = f'href="{lesson_detail_url}"'
        assertContains(response, href)


@pytest.mark.django_db
def test_delete_lesson_links_exist_in_subject_detail_for_teachers(client, teacher):
    EDIT_LESSON_URL = '/subjects/{subject_code}/lessons/{lesson_pk}/delete/'

    subject = baker.make_recipe('tests.subject', teacher=teacher)
    lessons = baker.make_recipe('tests.lesson', subject=subject, _quantity=10)
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/')
    assert response.status_code == HTTPStatus.OK
    for lesson in lessons:
        lesson_detail_url = EDIT_LESSON_URL.format(subject_code=subject.code, lesson_pk=lesson.pk)
        href = f'href="{lesson_detail_url}"'
        assertContains(response, href)


@pytest.mark.django_db
def test_add_lesson_displays_form_properly(client, teacher):
    subject = baker.make_recipe('tests.subject', teacher=teacher)
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/lessons/add/')
    assert response.status_code == HTTPStatus.OK
    form = response.context['form']
    assert 'title' in form.fields
    assert 'content' in form.fields


@pytest.mark.django_db
def test_add_lesson_works_properly(client, teacher, fake):
    subject = baker.make_recipe('tests.subject', teacher=teacher)
    client.force_login(teacher)
    title, content = fake.sentence(), fake.paragraph()
    payload = dict(title=title, content=content)
    response = client.post(f'/subjects/{subject.code}/lessons/add/', payload, follow=True)
    assertContains(response, 'Lesson was successfully added.')
    assertRedirects(response, f'/subjects/{subject.code}/')
    assert subject.lessons.get(title=title, content=content) is not None


@pytest.mark.django_db
def test_add_lesson_is_forbidden_for_non_teaching_teachers(client, teacher):
    subject = baker.make_recipe('tests.subject')
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/lessons/add/')
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_add_lesson_is_forbidden_for_students(client, teacher):
    subject = baker.make_recipe('tests.subject')
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/lessons/add/')
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_lesson_detail_for_teachers(client, teacher):
    subject = baker.make_recipe('tests.subject', teacher=teacher)
    lesson = baker.make_recipe('tests.lesson', subject=subject)
    client.force_login(teacher)
    url = f'/subjects/{subject.code}/lessons/{lesson.pk}/'
    response = client.get(url)
    assertContains(response, lesson.content)


@pytest.mark.django_db
def test_lesson_detail_is_forbidden_for_non_teaching_teachers(client, teacher):
    subject = baker.make_recipe('tests.subject')
    lesson = baker.make_recipe('tests.lesson', subject=subject)
    client.force_login(teacher)
    url = f'/subjects/{subject.code}/lessons/{lesson.pk}/'
    response = client.get(url)
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_lesson_detail_contains_edit_link_for_teachers(client, teacher):
    subject = baker.make_recipe('tests.subject', teacher=teacher)
    lesson = baker.make_recipe('tests.lesson', subject=subject)
    client.force_login(teacher)
    lesson_detail_url = f'/subjects/{subject.code}/lessons/{lesson.pk}/'
    lesson_edit_url = f'/subjects/{subject.code}/lessons/{lesson.pk}/edit/'
    response = client.get(lesson_detail_url)
    href = f'href="{lesson_edit_url}"'
    assertContains(response, href)


@pytest.mark.django_db
def test_lesson_detail_contains_delete_link_for_teachers(client, teacher):
    subject = baker.make_recipe('tests.subject', teacher=teacher)
    lesson = baker.make_recipe('tests.lesson', subject=subject)
    client.force_login(teacher)
    lesson_detail_url = f'/subjects/{subject.code}/lessons/{lesson.pk}/'
    lesson_edit_url = f'/subjects/{subject.code}/lessons/{lesson.pk}/delete/'
    response = client.get(lesson_detail_url)
    href = f'href="{lesson_edit_url}"'
    assertContains(response, href)


@pytest.mark.django_db
def test_edit_lesson_displays_form_properly(client, teacher):
    subject = baker.make_recipe('tests.subject', teacher=teacher)
    lesson = baker.make_recipe('tests.lesson', subject=subject)
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/lessons/{lesson.pk}/edit/')
    assert response.status_code == HTTPStatus.OK
    form = response.context['form']
    assert 'title' in form.fields
    assert 'content' in form.fields
    assertContains(response, lesson.title)
    assertContains(response, lesson.content)


@pytest.mark.django_db
def test_edit_lesson_works_properly(client, teacher, fake):
    subject = baker.make_recipe('tests.subject', teacher=teacher)
    lesson = baker.make_recipe('tests.lesson', subject=subject)
    client.force_login(teacher)
    title, content = fake.sentence(), fake.paragraph()
    payload = dict(title=title, content=content)
    url = f'/subjects/{subject.code}/lessons/{lesson.pk}/edit/'
    response = client.post(url, payload)
    assert response.status_code == HTTPStatus.OK
    assert (edited_lesson := subject.lessons.get(pk=lesson.pk)) is not None
    assert edited_lesson.title == title
    assert edited_lesson.content == content
    assertContains(response, 'Changes were successfully saved.')


@pytest.mark.django_db
def test_edit_lesson_is_forbidden_for_students(client, teacher):
    subject = baker.make_recipe('tests.subject')
    lesson = baker.make_recipe('tests.lesson', subject=subject)
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/lessons/{lesson.pk}/edit/')
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_edit_lesson_is_forbidden_for_non_teaching_teachers(client, teacher):
    subject = baker.make_recipe('tests.subject')
    lesson = baker.make_recipe('tests.lesson', subject=subject)
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/lessons/{lesson.pk}/edit/')
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_delete_lesson_works_properly(client, teacher):
    subject = baker.make_recipe('tests.subject', teacher=teacher)
    lesson = baker.make_recipe('tests.lesson', subject=subject)
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/lessons/{lesson.pk}/delete/', follow=True)
    assertContains(response, 'Lesson was successfully deleted.')
    assertRedirects(response, f'/subjects/{subject.code}/')
    assert subject.lessons.filter(pk=lesson.pk).count() == 0


@pytest.mark.django_db
def test_delete_lesson_is_forbidden_for_non_teaching_teachers(client, teacher):
    subject = baker.make_recipe('tests.subject')
    lesson = baker.make_recipe('tests.lesson', subject=subject)
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/lessons/{lesson.pk}/delete/')
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_delete_lesson_is_forbidden_for_students(client, teacher):
    subject = baker.make_recipe('tests.subject')
    lesson = baker.make_recipe('tests.lesson', subject=subject)
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/lessons/{lesson.pk}/delete/')
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_mark_list_displays_properly(client, teacher):
    subject = baker.make_recipe('tests.subject', teacher=teacher)
    enrollments = baker.make_recipe('tests.enrollment', subject=subject, _quantity=10)
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/marks/')
    for enrollment in enrollments:
        assertContains(response, enrollment.student)
        assertContains(response, enrollment.mark)


@pytest.mark.django_db
def test_mark_list_contains_link_to_edit_marks(client, teacher):
    subject = baker.make_recipe('tests.subject', teacher=teacher)
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/marks/')
    href = f'href="/subjects/{subject.code}/marks/edit/"'
    assertContains(response, href)


@pytest.mark.django_db
def test_mark_is_forbidden_for_non_teaching_teachers(client, teacher):
    subject = baker.make_recipe('tests.subject')
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/marks/')
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_mark_is_forbidden_for_students(client, teacher):
    subject = baker.make_recipe('tests.subject')
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/marks/')
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_mark_list_contains_links_to_each_student_profile(client, teacher):
    subject = baker.make_recipe('tests.subject', teacher=teacher)
    enrollments = baker.make_recipe('tests.enrollment', subject=subject, _quantity=10)
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/marks/')
    for enrollment in enrollments:
        href = f'href="/users/{enrollment.student.username}/"'
        assertContains(response, href)


@pytest.mark.django_db
def test_edit_marks_shows_marks_properly(client, teacher):
    subject = baker.make_recipe('tests.subject', teacher=teacher)
    enrollments = baker.make_recipe('tests.enrollment', subject=subject, _quantity=10)
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/marks/edit/')
    response_text = response.content.decode()
    for enrollment in enrollments:
        assert re.search(rf'value="{enrollment.mark}"', response_text, re.I | re.M | re.S)


@pytest.mark.django_db
def test_edit_marks_works_properly(client, teacher):
    subject = baker.make_recipe('tests.subject', teacher=teacher)
    enrollments = baker.make_recipe('tests.enrollment', subject=subject, _quantity=10)
    num_enrollments = len(enrollments)
    client.force_login(teacher)
    payload = {
        'form-TOTAL_FORMS': num_enrollments,
        'form-INITIAL_FORMS': num_enrollments,
        'form-MIN_NUM_FORMS': 0,
        'form-MAX_NUM_FORMS': 1000,
    }
    for enroll_idx, enrollment in enumerate(enrollments):
        payload[f'form-{enroll_idx}-id'] = enrollment.pk
        payload[f'form-{enroll_idx}-mark'] = random.randint(1, 10)
    response = client.post(f'/subjects/{subject.code}/marks/edit/', payload, follow=True)
    print(response.content)
    assert response.status_code == HTTPStatus.OK
    assertContains(response, 'Marks were successfully saved.')
    for enroll_idx in range(num_enrollments):
        enrollment_pk = payload[f'form-{enroll_idx}-id']
        mark = payload[f'form-{enroll_idx}-mark']
        assert Enrollment.objects.get(pk=enrollment_pk).mark == mark


@pytest.mark.django_db
def test_edit_is_forbidden_for_non_teaching_teachers(client, teacher):
    subject = baker.make_recipe('tests.subject')
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/marks/edit/')
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_edit_is_forbidden_for_students(client, teacher):
    subject = baker.make_recipe('tests.subject')
    client.force_login(teacher)
    response = client.get(f'/subjects/{subject.code}/marks/edit/')
    assert response.status_code == HTTPStatus.FORBIDDEN
