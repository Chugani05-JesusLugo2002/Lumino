from crispy_forms.layout import HTML, Field, Layout
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from django import forms
from django.core.exceptions import ValidationError

from .models import Enrollment, Lesson


class AddLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'content')

    def __init__(self, subject, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subject = subject
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title'),
            Field('content'),
            FormActions(
                HTML('<a class="btn btn-danger btn-lg" href="{{ subject.get_absolute_url }}"><i class="bi bi-arrow-left-circle"></i> Cancel</a>'),
                HTML('<button type="submit" class="btn btn-primary btn-lg"> <i class="bi bi-plus-circle"></i> Add </button>'), 
                css_class="mt-4 d-flex justify-content-between"
            ),
        )
    

    def save(self, *args, **kwargs):
        lesson = super().save(commit=False)
        lesson.subject = self.subject
        lesson = super().save(*args, **kwargs)
        return lesson


class EditLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = (
            'title', 
            'content',
        )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title'),
            Field('content'),
            FormActions(
                HTML('<a class="btn btn-danger btn-lg" href="{{ subject.get_absolute_url }}"><i class="bi bi-arrow-left-circle"></i> Cancel</a>'),
                HTML('<button type="submit" class="btn btn-primary btn-lg"> <i class="bi bi-check-circle"></i> Done </button>'),
                css_class="mt-4 d-flex justify-content-between"
            ),
        )


class EditMarkForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ('mark',)
        widgets = {'mark': forms.TextInput(attrs={'size': 3})}

    def clean_mark(self):
        mark = self.cleaned_data['mark']
        if mark:
            try:
                mark = int(mark)
            except ValueError:
                raise ValidationError('Mark must be a number or a blank space.')
            if not 0 <= mark <= 10:
                raise ValidationError('Mark is not between the allowed range (0-10)!')
        return mark
