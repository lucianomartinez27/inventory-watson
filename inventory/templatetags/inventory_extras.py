from django import template

register = template.Library()

@register.filter
def get_verbose_name(object): 
    return object._meta.verbose_name


@register.filter
def get_string_name(object): 
    return str(object)