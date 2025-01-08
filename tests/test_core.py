import pytest
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from pytest_django.asserts import assertRedirects

from subjects.models import Enrollment, Lesson, Subject
from users.models import Profile


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
def test_subject_model_has_proper_fields():
    PROPER_FIELDS = ('code', 'name', 'teacher', 'students')
    for field in PROPER_FIELDS:
        assert (
            getattr(Subject, field) is not None
        ), f'El campo <{field}> no está en el modelo Subject.'


@pytest.mark.django_db
def test_lesson_model_has_proper_fields():
    PROPER_FIELDS = ('subject', 'title', 'content')
    for field in PROPER_FIELDS:
        assert (
            getattr(Lesson, field) is not None
        ), f'El campo <{field}> no está en el modelo Lesson.'


@pytest.mark.django_db
def test_enrollment_model_has_proper_fields():
    PROPER_FIELDS = ('student', 'subject', 'enrolled_at', 'mark')
    for field in PROPER_FIELDS:
        assert (
            getattr(Enrollment, field) is not None
        ), f'El campo <{field}> no está en el modelo Enrollment.'


@pytest.mark.django_db
def test_profile_model_has_proper_fields():
    PROPER_FIELDS = ('user', 'role', 'bio', 'avatar')
    for field in PROPER_FIELDS:
        assert (
            getattr(Profile, field) is not None
        ), f'El campo <{field}> no está en el modelo Profile.'


@pytest.mark.django_db
def test_enrollment_model_has_proper_validators():
    validators = Enrollment.mark.field.validators
    assert (
        len(validators) == 2
    ), 'Debe haber dos validadores (min y max) para el campo "mark" de Enrollment.'
    if 'less' in validators[0].message:
        max_validator = validators[0]
        min_validator = validators[1]
    else:
        min_validator = validators[0]
        max_validator = validators[1]
    assert isinstance(min_validator, MinValueValidator)
    assert isinstance(max_validator, MaxValueValidator)
    assert min_validator.limit_value == 1
    assert max_validator.limit_value == 10


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
