from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Layout, Row, Submit, Div

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
            Div(
                HTML(
                    '<a class="btn btn-danger btn-lg" href="{{ subject.get_absolute_url }}"><i class="bi bi-arrow-left-circle"></i> Exit</a>'
                ),
                HTML(
                    '{% load editor_help from subject_extras %} {% editor_help %}'
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
        self.helper.form_class = "card shadow bg-light p-4 needs-validation"
        self.helper.attrs = dict(novalidate=True)
        self.helper.layout = Layout(
            Field('title'),
            Field('content'),
            Div(
                HTML(
                    '<a class="btn btn-danger btn-lg" href="{{ subject.get_absolute_url }}"><i class="bi bi-arrow-left-circle"></i> Exit</a>'
                ),
                HTML(
                    '{% load editor_help from subject_extras %} {% editor_help %}'
                ),
                HTML(
                    '<button type="submit" class="btn btn-primary btn-lg"> <i class="bi bi-check-circle"></i> Save </button>'
                ),
                css_class='mt-4 d-flex justify-content-between',
            ),
        )


class EditMarkForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['mark']


class EditMarkFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_show_labels = False
        self.layout = Layout(
            Row(
                HTML(
                    '{% load subject_extras %} <div class="col-md-2">{% edit_mark_student_label formset forloop.counter0 %}</div>'
                ),
                Field('mark', wrapper_class='col-md-2'),
                css_class='align-items-baseline',
            ),
        )
        self.add_input(Submit('save', 'Save marks', css_class='mt-3'))

class EnrollmentForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, user, enrolling=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'Enrollments' if enrolling else 'Unenrollments'
        self.fields['subjects'].queryset = self.choice_queryset(enrolling, user)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        action_label = 'Enroll' if enrolling else 'Unenroll'
        self.helper.layout = Layout(
            Field('subjects'),
            Div(
                HTML(
                    '<a class="btn btn-danger btn-lg" href="{% url "subjects:subject-list" %}"><i class="bi bi-arrow-left-circle"></i> Cancel</a>'
                ),
                HTML(
                    f'<button type="submit" class="btn btn-primary btn-lg mx-3"> <i class="bi bi-check-circle"></i> {action_label} </button>'
                ),
                css_class='mt-4',
            ),
        )
            
    def choice_queryset(self, is_enrolling, user):
        if is_enrolling:
            return self.fields['subjects'].queryset.exclude(pk__in=user.enrolled.all())
        return self.fields['subjects'].queryset.filter(pk__in=user.enrolled.all())

    def enrolls(self, user) -> None:
        subjects = self.cleaned_data['subjects']
        for subject in subjects:
            user.enrolled.add(subject)

    def unenrolls(self, user) -> None:
        subjects = self.cleaned_data['subjects']
        for subject in subjects:
            user.enrolled.remove(subject)
