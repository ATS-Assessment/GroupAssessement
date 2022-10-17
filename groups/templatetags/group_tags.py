from django import template

register = template.Library()


@register.filter
def current_user(value, args):
    if value.filter(member_id=args).exists():
        return True
    return False

