from django import template
from checkout.models import Rent

register = template.Library()


@register.filter(name='get_item')
def get_item(items, k):
    return items.get(k)


@register.filter(name='incr')
def incr(item):
    return item+1


@register.filter(name='dcr')
def dcr(item):
    return item-1


@register.filter(name='length')
def length(l):
    return len(l)


@register.filter(name='rent')
def rent(order_id):
    rent = Rent.objects.get(order_id=order_id)
    return rent


@register.simple_tag()
def assign(n):
    return n
