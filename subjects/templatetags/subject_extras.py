from django import template

from subjects.models import Enrollment

register = template.Library()


@register.inclusion_tag('subjects/components/mark_row.html')
def mark_row(enroll: Enrollment):
    student = enroll.student
    mark = enroll.mark
    css_class = ''
    if mark is not None:
        css_class = 'table-danger' if mark < 5 else 'table-success'
    else:
        mark = '-'
    return dict(student=student, mark=mark, css_class=css_class)


@register.inclusion_tag('subjects/components/student_label.html')
def student_label(student):
    avatar = student.profile.avatar
    name = student.username
    return dict(avatar=avatar, name=name)


@register.inclusion_tag('subjects/components/student_mark.html')
def student_mark(student, subject):
    enroll = Enrollment.objects.get(student=student, subject=subject)
    mark = enroll.mark
    css_class = ''
    if mark is not None:
        css_class = (
            'bg-danger-subtle text-danger-emphasis'
            if mark < 5
            else 'bg-success-subtle text-success-emphasis'
        )
    return dict(mark=mark, css_class=css_class)

@register.inclusion_tag('subjects/components/student_actions.html')
def student_actions(user):
    return dict(is_student=user.profile.is_student)