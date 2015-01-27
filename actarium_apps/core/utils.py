from django.utils.translation import ugettext as _
from actarium_apps.customers_services.models import Customers, CustomersServices, Services,  OrderStatus, CustomerOrders, OrderItems, Addresses, PaymentMethods
from actarium_apps.organizations.models import Organizations
from .models import *

import re
from django.db.models import Q


def create_default_service(user,org):
    from apps.website.views import getGlobalVar
    
    actarium_customer = ActariumCustomers.objects.get_or_none(user=user)
    if actarium_customer:
        customer = actarium_customer.customer
    else:
        address = Addresses.objects.create(country="",province="",city="")
        payment_method = PaymentMethods.objects.get_or_none(code="P001")
        if payment_method == None:
            return False, _(u"No se encontro el metodo de pago")
        customer = Customers.objects.create(name=user.get_full_name(),email=user.email,address=address)
        customer.payment_methods.add(payment_method)
        ActariumCustomers.objects.create(user=user,customer=customer)
    
    
    order_status = OrderStatus.objects.get_or_none(code="002", is_active=True)
    if order_status == None:
        return False, _(u"No existe estado de orden con el codigo 002")
    
    # Default Service
    FREE_SERVICE = getGlobalVar("FREE_SERVICE")
    service = Services.objects.get_or_none(code=FREE_SERVICE)
    if service == None:
        return False, _(u"No existe un servicio con el codigo proporcionado")
    customer_order = CustomerOrders.objects.create(customer=customer,status=order_status)
        
    import datetime
    from apps.website.views import getGlobalVar
    number_of_periods = int(getGlobalVar('TRIAL_MONTH'))
    number_of_members = int(getGlobalVar('TRIAL_MEMBERS'))
    date_expiration = datetime.date.today() + datetime.timedelta(number_of_periods*30,0,0)
    customer_service = CustomersServices.objects.create(quantity=number_of_members,date_expiration = date_expiration)
    
    OrderItems(service=service,
               order=customer_order,
               order_quantity=number_of_members, 
               number_of_periods=number_of_periods,
               customer_service= customer_service,
               discount = 0).save()
            
        
    try:
        OrganizationServices(organization=org,service=customer_service).save()
    except:
        return False, _(u"Error al intentar relacionar una organizacion con un servicio")
    
    return True, _(u"Se ha creado el servicio por defecto correctamente")



def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
