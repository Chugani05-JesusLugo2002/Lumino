import pytest
from django.conf import settings
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
def test_required_apps_are_installed():
    PROPER_APPS = ('accounts', 'shared', 'users', 'subjects')

    custom_apps = [app for app in settings.INSTALLED_APPS if not app.startswith('django')]
    for app in PROPER_APPS:
        app_config = f'{app}.apps.{app.title()}Config'
        assert (
            app_config in custom_apps
        ), f'La aplicación <{app}> no está "creada/instalada" en el proyecto.'
    assert len(custom_apps) >= len(
        PROPER_APPS
    ), 'El número de aplicaciones propias definidas en el proyecto no es correcto.'


@pytest.mark.django_db
def test_subject_model_has_proper_fields(subject):
    PROPER_FIELDS = ('code', 'name', 'teacher', 'students')
    for field in PROPER_FIELDS:
        assert (
            getattr(subject, field) is not None
        ), f'El campo <{field}> no está en el modelo Subject.'


@pytest.mark.django_db
def test_lesson_model_has_proper_fields(lesson):
    PROPER_FIELDS = ('subject', 'title', 'content')
    for field in PROPER_FIELDS:
        assert (
            getattr(lesson, field) is not None
        ), f'El campo <{field}> no está en el modelo Lesson.'


@pytest.mark.django_db
def test_enrollment_model_has_proper_fields(enrollment):
    PROPER_FIELDS = ('student', 'subject', 'enrolled_at', 'mark')
    for field in PROPER_FIELDS:
        assert (
            getattr(enrollment, field) is not None
        ), f'El campo <{field}> no está en el modelo Enrollment.'


@pytest.mark.django_db
def test_profile_model_has_proper_fields(profile):
    PROPER_FIELDS = ('user', 'role', 'bio', 'avatar')
    for field in PROPER_FIELDS:
        assert (
            getattr(profile, field) is not None
        ), f'El campo <{field}> no está en el modelo Profile.'


@pytest.mark.django_db
def test_models_are_available_on_admin(admin_client):
    MODELS = ('subjects.Subject', 'subjects.Lesson', 'subjects.Enrollment', 'users.Profile')

    for model in MODELS:
        url_model_path = model.replace('.', '/').lower()
        url = f'/admin/{url_model_path}/'
        response = admin_client.get(url)
        assert response.status_code == 200, f'El modelo <{model}> no está habilitado en el admin.'


# ==============================================================================
# Test urls with login required.
# ==============================================================================

AUTH_URLS = [
    # SUBJECTS
    '/subjects/',
    '/subjects/AAA/',
    '/subjects/AAA/lessons/add/',
    '/subjects/AAA/lessons/1/',
    '/subjects/AAA/lessons/17/edit/',
    '/subjects/AAA/lessons/17/delete/',
    '/subjects/AAA/marks/',
    '/subjects/AAA/marks/edit/',
    '/subjects/enroll/',
    '/subjects/unenroll/',
    # USERS
    '/users/guido/',
    '/user/edit/',
    '/user/leave/',
]

testdata = [(url, f'/login/?next={url}') for url in AUTH_URLS]


@pytest.mark.parametrize('auth_url, redirect_url', testdata)
@pytest.mark.django_db
def test_login_required(client, auth_url, redirect_url):
    response = client.get(auth_url, follow=True)
    assertRedirects(response, redirect_url)
