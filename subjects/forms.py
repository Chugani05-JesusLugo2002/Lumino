from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Layout, Row, Submit
from django import forms

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
            )
        )
        self.add_input(Submit('save', 'Save marks', css_class='mt-3'))
    


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
                pk__in=user.enrolled.all()
            )
        else:
            self.fields['subjects'].queryset = self.fields['subjects'].queryset.filter(
                pk__in=user.enrolled.all()
            )

    def enrolls(self, user):
        subjects = self.cleaned_data['subjects']
        for subject in subjects:
            user.enrolled.add(subject)

    def unenrolls(self, user):
        subjects = self.cleaned_data['subjects']
        for subject in subjects:
            user.enrolled.remove(subject)
