from django import template

register = template.Library()

@register.filter(name="exclude")
def exclude(value, arg):
    return value.replace(f'{arg} ', "")