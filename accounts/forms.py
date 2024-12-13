from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Layout
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from users.models import Profile


class LoginForm(forms.Form):
    username = forms.SlugField(max_length=64, required=True)
    password = forms.CharField(max_length=64, required=True, widget=forms.PasswordInput)

    def get_credentials(self):
        return self.cleaned_data['username'], self.cleaned_data['password']

    def __init__(self, subject, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subject = subject
        self.helper = FormHelper()
        self.helper.form_class = 'needs-validation'
        self.helper.layout = Layout(
            FloatingField('username'),
            FloatingField('password'),
            Div(
                HTML('<button type="submit" class="btn btn-primary w-100 mt-4">Login</button>'),
            ),
        )

    def clean_username(self):
        data = self.cleaned_data['username']
        if len(data) <= 0:
            return ValidationError('¿No tienes nombre?')
        return data


class SignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = dict(password=forms.PasswordInput)
        help_texts = dict(username=None)

    def __init__(self, subject, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subject = subject
        self.helper = FormHelper()
        self.helper.form_class = ''
        self.helper.layout = Layout(
            FloatingField('first_name'),
            FloatingField('last_name'),
            FloatingField('username'),
            FloatingField('email'),
            FloatingField('password'),
            Div(
                HTML('<button type="submit" class="btn btn-primary w-100 mt-4">Signup</button>'),
            ),
        )

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user = super().save(*args, **kwargs)
        Profile.objects.create(user=user)
        return user
