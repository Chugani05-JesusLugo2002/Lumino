from uuid import uuid4

from django import template
from django.urls import reverse

register = template.Library()


@register.inclusion_tag('components/modal.html')
def modal(
    btn_label: str,
    url: str,
    *url_args,
    title: str = 'Action',
    body: str = 'Are you sure?',
    css_class: str = 'btn btn-primary',
    modal_btn_label: str = 'Action',
):
    modal_id = uuid4()
    url = reverse(url, args=url_args)
    return dict(
        modal_id=modal_id,
        title=title,
        body=body,
        url=url,
        btn_label=btn_label,
        css_class=css_class,
        modal_btn_label=modal_btn_label,
    )


@register.inclusion_tag('components/alert.html')
def alert(text: str):
    return dict(text=text)

@register.inclusion_tag('components/user-subject-list.html')
def user_subject_list(user):
    subjects = user.profile.get_subjects()
    return dict(subjects=subjects)