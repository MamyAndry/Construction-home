from django import template

register = template.Library()

@register.filter
def substract(value, arg):
    if arg is None:
        arg = 0
    if value is None:
        value = 0
    res = value - arg
    return f"{res:,.2f}"