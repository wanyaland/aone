from django import template

register = template.Library()

@register.filter
def get_popularity(value):
    return range(value)

@register.filter
def get_range(value):
    return range(1,value)

@register.filter
def list_categories(value):
    return ','.join(str(x) for x in value)