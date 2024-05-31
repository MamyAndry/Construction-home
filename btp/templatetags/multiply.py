from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    if arg is None:
        arg = 0
    if value is None:
        value = 0
    return value * arg