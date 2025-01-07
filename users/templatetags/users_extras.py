from django import template

register = template.Library()

@register.filter
def fullname(user) -> str:
    return f'{user.first_name} {user.last_name}'