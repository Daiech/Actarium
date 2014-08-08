# encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.utils.translation import ugettext as _
from .models import OrderItems, OrderStatus
import json
import datetime


def approve_order(request):
    # if request.is_ajax():
    if request.user.is_staff:
        if request.method == "POST":
            order_id = request.POST.get('order_id')
            order_item =  OrderItems.objects.get_or_none(id=order_id)
            if order_item:
                status_approve = OrderStatus.objects.get(code="002")
                status_defeated = OrderStatus.objects.get(code="006")
                print status_approve
                print status_defeated
                
                last_order = order_item.customer_service.get_order_active()

                if last_order.service.code=="S000":

                    new_order = order_item

                    if last_order:
                        last_customer_order = last_order.order
                        last_customer_order.status = status_defeated
                        last_customer_order.save()

                    new_customer_order = new_order.order
                    new_customer_order.status = status_approve
                    new_customer_order.save()

                    customer_service = order_item.customer_service
                    customer_service.quantity = new_order.order_quantity
                    number_of_periods = new_order.number_of_periods
                    print "number_of_periods", number_of_periods
                    date_expiration = datetime.date.today() + datetime.timedelta(number_of_periods*30,0,0)
                    print date_expiration
                    customer_service.date_expiration = date_expiration
                    customer_service.save()

                    message = {'is_done':True,'response':_("Modificado Correctamente")}
                    print message
                else:
                    message = {'Error': _(u"Opción no implementada, únicamente se puede actualizar la version trial" )}
                    print message['Error']
            else:
                message = {'Error': _( "No hay orden disponible" )}
                print message['Error']
    else:
        message = {'Error': _( u"No tiene permiso para realizar esta acción" )}
        print message['Error']
        
    return HttpResponse(json.dumps(message), mimetype="application/json")
    