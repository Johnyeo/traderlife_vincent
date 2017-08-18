# coding:utf-8
from django import template
#

register = template.Library()

def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')

# A tuple of standard large number to their converters


@register.filter(is_safe=False)
def kmgnumber(value):
    if value < 1000:
        return value
    elif value < 1000000:
        value = value / 1000
        value = "%.2fk" % value
        return value
    elif value < 1000000000:
        value = value / 1000000
        value = "%.2fm" % value
        return value
    elif value < 1000000000000:
        value = value / 1000000000
        value = "%.2fb" % value
        return value
    else:
        return "大数"