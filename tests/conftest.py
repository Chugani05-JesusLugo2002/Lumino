import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from model_bakery import baker
from PIL import Image

from users.models import Profile


@pytest.fixture
def user(django_user_model):
    return baker.make(django_user_model, _fill_optional=True)


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
    return user


@pytest.fixture
def another_student(django_user_model):
    user = baker.make(django_user_model, _fill_optional=True)
    return user


@pytest.fixture
def teacher(django_user_model):
    user = baker.make(django_user_model, _fill_optional=True)
    user.profile.role = Profile.Role.TEACHER
    user.profile.save()
    return user


@pytest.fixture
def another_teacher(django_user_model):
    user = baker.make(django_user_model, _fill_optional=True)
    user.profile.role = Profile.Role.TEACHER
    user.profile.save()
    return user


@pytest.fixture
def image():
    img = Image.new('RGBA', size=(200, 200), color='white')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return SimpleUploadedFile(
        name='test_image.png',
        content=buffer.getvalue(),
        content_type='image/png',
    )
