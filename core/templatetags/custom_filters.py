# core/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def to_list(value, arg):
    return list(range(value, arg+1))
