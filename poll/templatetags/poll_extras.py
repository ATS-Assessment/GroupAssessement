from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def order_by(queryset, args):
    return queryset.order_by(*args)
