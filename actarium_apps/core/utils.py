from actarium_apps.customers_services.models import Customers, CustomersServices, Services,  OrderStatus, CustomerOrders, OrderItems, Addresses, PaymentMethods
from actarium_apps.organizations.models import Organizations
from .models import *


def create_default_service(user,org):
        actarium_customer = ActariumCustomers.objects.get_or_none(user=user)
        if actarium_customer:
            customer = actarium_customer.customer
        else:
            address = Addresses.objects.create(country="",province="",city="")
            payment_method = PaymentMethods.objects.get_or_none(code="P001")
            if payment_method == None:
                return False, "No se encontro el metodo de pago"
            customer = Customers.objects.create(name=user.get_full_name(),email=user.email,address=address)
            customer.payment_methods.add(payment_method)
            ActariumCustomers.objects.create(user=user,customer=customer)
        
        
        order_status = OrderStatus.objects.get_or_none(code="002", is_active=True)
        if order_status == None:
            return False, "No existe estado de orden con el codigo 002"
        
        
        service = Services.objects.get_or_none(code="S000")
        if service == None:
            return False, "No existe un servicio con el codigo proporcionado"
        customer_order = CustomerOrders.objects.create(customer=customer,status=order_status)
            
        import datetime
        number_of_periods = 3
        date_expiration = datetime.date.today() + datetime.timedelta(number_of_periods*30,0,0)
        customer_service = CustomersServices.objects.create(quantity=5,date_expiration = date_expiration)
        
        OrderItems(service=service,
                   order=customer_order,
                   order_quantity=5, 
                   number_of_periods=number_of_periods,
                   customer_service= customer_service,
                   discount = 0).save()
                
            
        try:
            OrganizationServices(organization=org,service=customer_service).save()
        except:
            return False, "Error al intentar relacionar una organizacion con un servicio"
        
        return True, "Se ha creado el servicio por defecto correctamente"