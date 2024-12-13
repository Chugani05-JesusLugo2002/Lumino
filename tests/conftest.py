import pytest
from faker import Faker
from model_bakery import baker

from users.models import Profile


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
    return baker.make_recipe('tests.subject', _fill_optional=True)


@pytest.fixture
def lesson():
    return baker.make('subjects.Lesson', _fill_optional=True)


@pytest.fixture
def enrollment():
    return baker.make_recipe('tests.enrollment', _fill_optional=True)


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


@pytest.fixture
def student(django_user_model):
    user = baker.make(django_user_model, _fill_optional=True)
    baker.make(Profile, user=user, role=Profile.Role.STUDENT, _fill_optional=True)
    return user


@pytest.fixture
def another_student(django_user_model):
    user = baker.make(django_user_model, _fill_optional=True)
    baker.make(Profile, user=user, role=Profile.Role.STUDENT, _fill_optional=True)
    return user


@pytest.fixture
def teacher(django_user_model):
    user = baker.make(django_user_model, _fill_optional=True)
    baker.make(Profile, user=user, role=Profile.Role.TEACHER, _fill_optional=True)
    return user


@pytest.fixture
def another_teacher(django_user_model):
    user = baker.make(django_user_model, _fill_optional=True)
    baker.make(Profile, user=user, role=Profile.Role.TEACHER, _fill_optional=True)
    return user
