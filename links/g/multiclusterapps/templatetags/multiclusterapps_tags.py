from django import template
register = template.Library()


@register.simple_tag
def dictKeyLookup(dictionary, key):
    return dictionary.get(key, '')
