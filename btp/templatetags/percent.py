from django import template

register = template.Library()

@register.filter
def percent(total, partial):
    if(partial is None):
        return f"{0:,.2f}"
    res = (partial/total)*100
    return f"{res:,.2f}"
