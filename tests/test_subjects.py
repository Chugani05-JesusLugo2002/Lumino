import pytest
from model_bakery import baker
from pytest_django.asserts import assertContains, assertNotContains


@pytest.mark.dependency()
@pytest.mark.django_db
def test_subject_list_for_student(client, student, another_student):
    own_enrollments = baker.make_recipe('tests.enrollment', student=student, _quantity=10)
    another_enrollments = baker.make_recipe(
        'tests.enrollment', student=another_student, _quantity=10
    )
    client.force_login(student)
    response = client.get('/subjects/')
    for enrollment in own_enrollments:
        assertContains(response, enrollment.subject.code)
    for enrollment in another_enrollments:
        assertNotContains(response, enrollment.subject.code)


@pytest.mark.dependency(depends=['test_subject_list_for_student'])
@pytest.mark.django_db
def test_subject_list_for_student_contains_links_for_subject_details(client, student):
    SUBJECT_DETAIL_URL = '/subjects/{subject_code}/'
    enrollments = baker.make_recipe('tests.enrollment', student=student, _quantity=10)
    client.force_login(student)
    response = client.get('/subjects/')
    for enrollment in enrollments:
        href = f'href="{SUBJECT_DETAIL_URL.format(subject_code=enrollment.subject.code)}"'
        assertContains(response, href)


@pytest.mark.dependency()
@pytest.mark.django_db
def test_subject_list_for_teacher(client, teacher, another_teacher):
    own_teaching = baker.make_recipe('tests.subject', teacher=teacher, _quantity=10)
    another_teaching = baker.make_recipe('tests.subject', teacher=another_teacher, _quantity=10)
    client.force_login(teacher)
    response = client.get('/subjects/')
    for teaching in own_teaching:
        assertContains(response, teaching.code)
    for teaching in another_teaching:
        assertNotContains(response, teaching.code)
