from django import template

register = template.Library()

@register.filter
def fullname(user) -> str:
    return f'{user.first_name.title()} {user.last_name.title()}'