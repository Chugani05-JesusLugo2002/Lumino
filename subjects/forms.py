from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Layout
from django import forms
from django.core.exceptions import ValidationError

from .models import Enrollment, Lesson, Subject


class AddLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'content')

    def __init__(self, subject, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subject = subject
        self.helper = FormHelper()
        self.helper.form_class = 'needs-validation card shadow bg-light p-4'
        self.helper.layout = Layout(
            Field('title'),
            Field('content'),
            FormActions(
                HTML(
                    '<a class="btn btn-danger btn-lg" href="{{ subject.get_absolute_url }}"><i class="bi bi-arrow-left-circle"></i> Cancel</a>'
                ),
                HTML(
                    '<button type="submit" class="btn btn-primary btn-lg"> <i class="bi bi-plus-circle"></i> Add </button>'
                ),
                css_class='mt-4 d-flex justify-content-between',
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
                HTML(
                    '<a class="btn btn-danger btn-lg" href="{{ subject.get_absolute_url }}"><i class="bi bi-arrow-left-circle"></i> Cancel</a>'
                ),
                HTML(
                    '<button type="submit" class="btn btn-primary btn-lg"> <i class="bi bi-check-circle"></i> Done </button>'
                ),
                css_class='mt-4 d-flex justify-content-between',
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
            mark = int(mark)
            if not 0 <= mark <= 10:
                raise ValidationError('Mark is not between the allowed range (0-10)!')
        return mark


class EnrollmentForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, user, enrolling=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        action_label = 'Enroll' if enrolling else 'Unenroll'
        self.helper.layout = Layout(
            Field('subjects'),
            FormActions(
                HTML(
                    '<a class="btn btn-danger btn-lg" href="{% url "subjects:subject-list" %}"><i class="bi bi-arrow-left-circle"></i> Cancel</a>'
                ),
                HTML(
                    f'<button type="submit" class="btn btn-primary btn-lg"> <i class="bi bi-check-circle"></i> {action_label} </button>'
                ),
                css_class='mt-4 d-flex justify-content',
            ),
        )
        if enrolling:
            self.fields['subjects'].queryset = self.fields['subjects'].queryset.exclude(
                pk__in=user.student_subjects.all()
            )
        else:
            self.fields['subjects'].queryset = self.fields['subjects'].queryset.filter(
                pk__in=user.student_subjects.all()
            )

    def enrolls(self, user):
        subjects = self.cleaned_data['subjects']
        for subject in subjects:
            user.student_subjects.add(subject)

    def unenrolls(self, user):
        subjects = self.cleaned_data['subjects']
        for subject in subjects:
            user.student_subjects.remove(subject)
