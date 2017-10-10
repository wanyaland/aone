from django.template import Library

register = Library()


@register.filter("range")
def filter_range(start, end):
    return range(start, end)
