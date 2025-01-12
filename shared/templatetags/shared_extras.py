from django import template
from django.urls import reverse
from django.utils.translation import get_language

from uuid import uuid4

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

@register.inclusion_tag('components/setlang.html', takes_context=True)
def setlang(context):
    LANGUAGES = {
        'en': '🇺🇸',
        'es': '🇪🇸',
        'hi': '🇮🇳',
        'es-ve': '🇻🇪'
    }

    current_lang = get_language()
    current_flag = LANGUAGES.pop(current_lang)
    next = context['request'].path
    return {
        'current_lang': current_lang,
        'current_flag': current_flag,
        'languages': LANGUAGES,
        'next': next,
    }

@register.inclusion_tag('components/navigation-subject-list.html')
def navigation_subject_list(user):
    subjects = user.profile.get_subjects()
    return dict(subjects=subjects)