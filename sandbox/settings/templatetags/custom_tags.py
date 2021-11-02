from django import template
register = template.Library()


@register.filter(name='times')
def times(number):
    if (number is None):
        return None
    number += 1
    return range(1,int(number))

