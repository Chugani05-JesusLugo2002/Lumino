from django import template
from uuid import uuid4

register = template.Library()

@register.inclusion_tag('components/modal.html')
def modal(button_label: str = 'Action', title: str = 'Action', body: str = 'Are you sure?', url: str = '', css_class: str = 'btn btn-primary', modal_button_label: str = 'Action'):
    modal_id = uuid4()
    return dict(modal_id=modal_id, title=title, body=body, url=url, button_label=button_label, css_class=css_class, modal_button_label=modal_button_label)