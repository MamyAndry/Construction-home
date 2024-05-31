from django import template

register = template.Library()

@register.filter
def multiply(value):
    return f"{value:,.2f}"