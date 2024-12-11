from django import forms
from django.contrib.auth import get_user_model

from users.models import Profile


class LoginForm(forms.Form):
    username = forms.SlugField(max_length=64, required=True)
    password = forms.CharField(max_length=64, required=True, widget=forms.PasswordInput)

    def get_credentials(self):
        return self.cleaned_data['username'], self.cleaned_data['password']


class SignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = dict(password=forms.PasswordInput)
        help_texts = dict(username=None)

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user = super().save(*args, **kwargs)
        Profile.objects.create(user=user)
        return user
