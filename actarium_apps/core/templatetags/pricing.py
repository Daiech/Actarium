#encoding:utf-8
from ..models import ServicesRanges
from django.template import Library


register = Library()


@register.filter
def total_price(quantity):
    quantity = int(quantity)
    total_price = ServicesRanges.objects.get_total_price(quantity)
    return total_price
       
