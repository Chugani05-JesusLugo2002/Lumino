from django import template

from subjects.models import Enrollment

register = template.Library()

@register.inclusion_tag('subjects/components/mark_row.html')
def mark_row(enroll: Enrollment):
    student = enroll.student
    mark = enroll.mark
    css_class = ''
    if mark:
        css_class = 'table-danger' if mark < 5 else 'table-success'
    else:
        mark = '-'
    return dict(student=student, mark=mark, css_class=css_class)