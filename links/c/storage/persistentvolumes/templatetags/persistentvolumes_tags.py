from django import template


register = template.Library()


@register.simple_tag
def lookup(dictionary, key):
    return dictionary.get(key, '')


@register.filter
def hyphen(left, right):
    return str(left) + "-" + str(right)


@register.filter
def get(dictionary, key):
    return dictionary.get(key, '')
