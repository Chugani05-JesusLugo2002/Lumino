from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField

from users.models import Profile    


class LoginForm(forms.Form):
    username = forms.SlugField(max_length=64, required=True)
    password = forms.CharField(max_length=64, required=True, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True)
        self.helper.form_class = 'card-body p-5 shadow rounded bg-light overflow-auto'
        self.helper.layout = Layout(
            HTML('<h3 class="card-title text-center mb-4">Login</h3>'),
            FloatingField('username'),
            FloatingField('password'),
            HTML('<p class="text-secondary">Fields with * are required.</p>'),
            Submit('login', 'Login', css_class="btn btn-primary btn-block w-100"),
            HTML('<p class="text-center mt-4">No account? <a href="{% url "signup" %}" class="link-primary text-decoration-none">Create one!</a></p>')
        )

    def get_credentials(self):
        return self.cleaned_data['username'], self.cleaned_data['password']


class SignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = dict(password=forms.PasswordInput)
        help_texts = dict(username=None)

    def make_fields_required(self):
        for field in self.fields:
            self.fields[field].required = True
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.make_fields_required()
        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True)
        self.helper.form_class = 'card-body px-5 py-4 rounded bg-light'
        self.helper.layout = Layout(
            HTML('<h3 class="card-title text-center mb-4">Signup</h3>'),
            FloatingField('first_name'),
            FloatingField('last_name'),
            FloatingField('username'),
            FloatingField('email'),
            FloatingField('password'),
            HTML('<p class="text-secondary">Fields with * are required.</p>'),
            Submit('signup', 'Signup', css_class='btn btn-primary w-100'),
            HTML('''<p class="text-center mt-4">
                Already have an account? 
                <a href="{% url "login" %}" class="link-primary text-decoration-none">Login here!</a>
            </p>'''),
        )
        

    def clean(self):
       User = get_user_model()
       email = self.cleaned_data.get('email')
       username = self.cleaned_data.get('username')
       if User.objects.filter(email=email).exists():
            raise ValidationError("An error, email exists!")
       if User.objects.filter(username=username).exists():
            raise ValidationError("An error, username exists!") 
       return self.cleaned_data
    
    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user = super().save(*args, **kwargs)
        Profile.objects.create(user=user)
        return user
