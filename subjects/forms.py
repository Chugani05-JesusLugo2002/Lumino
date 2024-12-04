from django import forms
from django.core.exceptions import ValidationError

from .models import Lesson, Enrollment


class AddLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'content')

    def __init__(self, subject, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subject = subject

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
        fields = 'mark',
        widgets = {
            'mark': forms.TextInput(attrs={'size': 3})
        }
    
    def clean_mark(self):
        mark = self.cleaned_data["mark"]
        if mark:
            try:
                mark = int(mark)
            except ValueError:
                raise ValidationError('Mark must be a number or a blank space.')
            if not 0 <= mark <= 10:
                raise ValidationError('Mark is not between the allowed range (0-10)!')
        return mark
    
