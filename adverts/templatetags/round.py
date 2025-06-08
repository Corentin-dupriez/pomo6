from django import template

register = template.Library()

@register.filter(name='round')
def round_filter(value):
    return int(value)