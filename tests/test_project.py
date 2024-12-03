import pytest
from django.conf import settings
from faker import Faker
from model_bakery import baker
from pytest_django.asserts import assertContains, assertRedirects

from subjects.models import Lesson, Subject
from users.models import Enrollment, Profile

# ==============================================================================
# FIXTURES
# ==============================================================================


@pytest.fixture
def user(django_user_model):
    return baker.make(django_user_model, _fill_optional=True)


@pytest.fixture
def user_with_profile(django_user_model):
    user = baker.make(django_user_model, _fill_optional=True)
    baker.make(Profile, user=user, _fill_optional=True)
    return user


@pytest.fixture
def subject():
    return baker.make(Subject, _fill_optional=True)


@pytest.fixture
def lesson():
    return baker.make(Lesson, _fill_optional=True)


@pytest.fixture
def enrollment():
    return baker.make(Enrollment, _fill_optional=True)


@pytest.fixture
def profile():
    return baker.make(Profile, _fill_optional=True)


@pytest.fixture
def fake():
    return Faker()


@pytest.fixture
def login_data(fake):
    return {
        'username': fake.user_name(),
        'password': fake.password(),
    }


@pytest.fixture
def signup_data(fake):
    return {
        'username': fake.user_name(),
        'password': fake.password(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
    }


# ==============================================================================
# TESTS
# ==============================================================================


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
def test_login_displays_correct_form(client, login_data):
    response = client.get('/login/')
    assert response.status_code == 200
    for field in login_data.keys():
        assertContains(response, field)


@pytest.mark.django_db
def test_login_works(client, login_data, django_user_model):
    REDIRECT_URL = '/subjects/'

    user = django_user_model.objects.create_user(
        username=login_data['username'], password=login_data['password']
    )
    baker.make(Profile, user=user)
    response = client.post(
        '/login/',
        dict(username=login_data['username'], password=login_data['password']),
        follow=True,
    )
    assertRedirects(response, REDIRECT_URL)


@pytest.mark.django_db
def test_login_fails_when_wrong_credentials_are_given(client, login_data, django_user_model):
    django_user_model.objects.create_user(
        username=login_data['username'], password=login_data['password']
    )
    response = client.post(
        '/login/', dict(username=login_data['username'], password=login_data['password'] + 'pytest')
    )
    assert response.status_code == 200
    assertContains(response, 'username')
    assertContains(response, 'password')


@pytest.mark.django_db
def test_login_contains_a_link_to_sign_up(client):
    response = client.get('/login/')
    assertContains(response, 'href="/signup/"')


@pytest.mark.django_db
def test_logout(client, user):
    client.force_login(user)
    client.get('/logout/')
    # https://stackoverflow.com/a/6013115
    assert '_auth_user_id' not in client.session, 'El usuario sigue logeado tras hacer "logout".'


@pytest.mark.django_db
def test_signup_displays_correct_form(client, signup_data):
    response = client.get('/signup/')
    assert response.status_code == 200
    for field in signup_data.keys():
        assertContains(response, field)


@pytest.mark.django_db
def test_signup_fails_when_any_field_is_not_provided(client, signup_data):
    for field in signup_data.keys():
        payload = signup_data.copy()
        payload.pop(field)
        response = client.post('/signup/', payload)
        assert response.status_code == 200
        assertContains(response, 'error')


@pytest.mark.django_db
def test_signup_fails_when_any_unique_field_is_duplicated(client, signup_data, user):
    UNIQUE_FIELDS = ('username', 'email')

    for field in UNIQUE_FIELDS:
        payload = signup_data.copy()
        payload[field] = getattr(user, field)
        response = client.post('/signup/', payload)
        assert response.status_code == 200
        assertContains(response, 'error')


@pytest.mark.django_db
def test_signup_works(client, signup_data, django_user_model):
    REDIRECT_URL = '/subjects/'

    response = client.post('/signup/', signup_data, follow=True)
    User = django_user_model
    signup_data.pop('password')
    user = User.objects.get(**signup_data)
    assert user.profile is not None, 'No se ha creado el perfil de usuario'
    assert (
        user.profile.role == Profile.Role.STUDENT
    ), 'El rol del usuario creado debe ser ESTUDIANTE'
    assertRedirects(response, REDIRECT_URL)


@pytest.mark.django_db
def test_signup_contains_a_link_to_login(client):
    response = client.get('/signup/')
    assertContains(response, 'href="/login/"')


@pytest.mark.django_db
def test_models_are_available_on_admin(admin_client):
    MODELS = ('subjects.Subject', 'subjects.Lesson', 'users.Profile', 'users.Enrollment')

    for model in MODELS:
        url_model_path = model.replace('.', '/').lower()
        url = f'/admin/{url_model_path}/'
        response = admin_client.get(url)
        assert response.status_code == 200, f'El modelo <{model}> no está habilitado en el admin.'
