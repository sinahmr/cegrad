from django import template
register = template.Library()

@register.filter
def percent(value, arg):
    try:
        return 100 * int(value) / (int(arg) + int(value))
    except (ValueError, ZeroDivisionError):
        return None