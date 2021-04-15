import re

from django import template

template.base.tag_re = re.compile(template.base.tag_re.pattern, re.DOTALL)
register = template.Library()


@register.filter
def get(dictionary, key):
    return dictionary.get(key, '')


@register.filter
def first(dictionary, key):
    first_key = list(dictionary.keys())[0]

    try:
        return dictionary[first_key].get(key, '')
    except:
        return ''
