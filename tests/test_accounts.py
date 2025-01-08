import pytest
from pytest_django.asserts import assertContains, assertRedirects

from users.models import Profile


@pytest.mark.django_db
def test_login_displays_correct_form(client, login_data):
    response = client.get('/login/')
    assert response.status_code == 200
    for field in login_data.keys():
        assertContains(response, field)


@pytest.mark.django_db
def test_login_works(client, login_data, django_user_model):
    REDIRECT_URL = '/subjects/'

    django_user_model.objects.create_user(
        username=login_data['username'], password=login_data['password']
    )
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
def test_signup_contains_a_link_to_login(client):
    response = client.get('/signup/')
    assertContains(response, 'href="/login/"')


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
def test_signup_shows_welcome_message(client, signup_data):
    REDIRECT_URL = '/subjects/'

    response = client.post('/signup/', signup_data, follow=True)
    assertRedirects(response, REDIRECT_URL)
    assertContains(response, 'Welcome to Lumino. Nice to see you!')
