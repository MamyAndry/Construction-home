
from django import template
from django.utils.translation import to_locale, get_language
from babel.numbers import format_number

register = template.Library()

def sexy_number(context, number, locale=None):
    if locale is None:
        locale = to_locale(get_language())
    return format_number(number, locale=locale)

register.simple_tag(takes_context=True)(sexy_number)