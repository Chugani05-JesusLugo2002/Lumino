from django import forms

from .models import Lesson


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
