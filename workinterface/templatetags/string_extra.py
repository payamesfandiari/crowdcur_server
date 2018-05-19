
from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def concat(value, arg):
    """Removes all values of arg from the given string"""
    return value + str(arg)