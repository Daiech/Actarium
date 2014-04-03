#encoding:utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

class GenericManager(models.Manager):

    def get_all_active(self):
        return self.filter(is_active=True).distinct().order_by('-modified')

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
        except self.model.MultipleObjectsReturned:
            return None

    def get_active_or_none(self, **kwargs):
        return self.get_or_none(is_active=True, **kwargs)

class OrderItemsManager(GenericManager):
    
    def create_members_order(self,number_of_members,number_of_months,customer_services,service,discount_value,user):
        id_order = None
        if customer_services and service:
            customer = user.actariumcustomers_user.all()[0].customer
            if customer:
                from .models import OrderStatus
                status = OrderStatus.objects.get_or_none(pk=1)
                if status:
                    from .models import CustomerOrders
                    customer_orders = CustomerOrders.objects.create(status=status, customer=customer)
                    try:
                        from .models import OrderItems
                        order_items = OrderItems(service=service,
                                            order=customer_orders,
                                            order_quantity=number_of_members,
                                            number_of_periods=number_of_months,
                                            customer_service=customer_services,
                                            discount=discount_value)
                        customer_orders.save()
                        order_items.save()
                        message = _("Pedido realizado Exitosamente")
                        id_order = order_items.id
                    except:
                        message = _("Error Creando objeto OrderItems")
                        customer_orders.delete()
                else:
                    message =  _("No Status")
            else:
                message = _("No customer")
        else:
            message = _("No customer services")
        
        return id_order, message
    
class CustomersServicesManager(GenericManager):
    pass

class ServicesManager(GenericManager):
    def get_all_active_orderer(self):
        return self.filter(is_active=True).distinct().order_by('code')