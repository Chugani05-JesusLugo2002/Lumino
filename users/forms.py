from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Layout
from django import forms

from .models import Profile


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'avatar',
            'bio',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('avatar'),
            Field('bio'),
            FormActions(
                HTML(
                    '<a class="btn btn-danger btn-lg" href="{{ subject.get_absolute_url }}"><i class="bi bi-arrow-left-circle"></i> Cancel</a>'
                ),
                HTML(
                    '<button type="submit" class="btn btn-primary btn-lg"> <i class="bi bi-check-circle"></i> Done </button>'
                ),
                css_class='mt-4 d-flex justify-content-between',
            ),
        )
