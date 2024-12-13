from uuid import uuid4

from django import template

register = template.Library()


@register.inclusion_tag('components/modal.html')
def modal(
    btn_label: str = 'Action',
    url: str = '',
    *url_args,
    title: str = 'Action',
    body: str = 'Are you sure?',
    css_class: str = 'btn btn-primary',
    modal_btn_label: str = 'Action',
):
    modal_id = uuid4()
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
