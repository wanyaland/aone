from django import template

register = template.Library()

@register.filter
def get_popularity(value):
    return range(value)

@register.filter
def get_range(value):
    return range(1,value)