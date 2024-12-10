# from crispy_forms.layout import HTML, Field, Layout, Submit
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
        # self.helper.layout = Layout(
        #     Field('title'),
        #     Field('content'),
        #     FormActions(
        #         Submit('add', 'Add', css_class='btn btn-danger btn-lg'),
        #         HTML(
        #             '<a class="btn btn-danger btn-lg" href="{{ subject.get_absolute_url }}"><i class="bi bi-arrow-left-circle"></i> Cancel</a>'
        #         ),
        #     ),
        # )
    

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
