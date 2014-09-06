#encoding:utf-8
from ..models import ServicesRanges
from django.template import Library


register = Library()


@register.filter
def total_price(quantity):
    total_price = ServicesRanges.objects.get_total_price(int(quantity))
    return int(total_price)

       
@register.filter
def icon_status(status_id):
    print status_id
    icon_status = ""
    if status_id== 1:
        icon_status = 'glyphicon-arrow-up'                    
    elif status_id == 2:
        icon_status = 'glyphicon-ok'
    elif status_id == 6:
        icon_status = 'glyphicon-trash'
    # return '<span class="glyphicon '+icon_status+'"></span>'
    return icon_status