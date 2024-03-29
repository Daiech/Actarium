#encoding:utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import *

# common fields: for use it uncomment the class below 
# and change "models.Model" for "CommonFields" in each class model that you want, 
# as well comment the attrs "is_active","created" and "modified" in each class 

#class CommonFields(models.Model):
#    is_active = models.BooleanField(default=True)
#    created = models.DateTimeField(auto_now_add=True)
#    modified = models.DateTimeField(auto_now=True)
#
#    class meta:
#        abstract = True

# models that require fixtures


class OrderStatus(models.Model):
    code = models.CharField(max_length=300, verbose_name=_(u"Código"))
    name = models.CharField(max_length=300, verbose_name=_("Nombre"))
    description = models.TextField(blank=True, verbose_name=_(u"Descripción"))
    is_active = models.BooleanField(default=True)
    
    objects = GenericManager()
    
    def __unicode__(self):
        return u"[%s] %s" % (self.code,self.name)


class Periods(models.Model):
    code = models.CharField(max_length=300, verbose_name=_(u"Código"))
    name = models.CharField(max_length=300, verbose_name=_("Nombre"))
    is_active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return u"[%s] %s" % (self.code,self.name)


# models that require Django-Admin


class ServicesCategories(models.Model,):
    code = models.CharField(max_length=100, verbose_name=_(u"Código"))
    name = models.CharField(max_length=300, verbose_name=_("Nombre"))
    description = models.TextField(blank=True, verbose_name=_(u"Descripción"))
    
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    objects = GenericManager()

    def __unicode__(self):
        return u"[%s] %s" % (self.code,self.name)


class PaymentMethods(models.Model):
    code = models.CharField(max_length=100, verbose_name=_(u"Código"))
    name = models.CharField(max_length=300, verbose_name=_("Nombre"))
    description = models.TextField(blank=True, verbose_name=_(u"Descripción"))
    
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    objects = GenericManager()

    def __unicode__(self):
        return u"%s" % (self.name)
    
    
class Services(models.Model):
    code = models.CharField(max_length=300, verbose_name=_(u"Código"))
    name = models.CharField(max_length=300, verbose_name=_("Nombre"))
    description = models.TextField(blank=True, verbose_name=_(u"Descripción"))
    price_per_period = models.FloatField(verbose_name=_(u"Precio por período"))
    
    period = models.ForeignKey(Periods, related_name='%(class)s_period', verbose_name=_(u"Período"))
    service_category = models.ForeignKey(ServicesCategories, related_name='%(class)s_service_category', verbose_name=_(u"Categoría"))

    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    objects = ServicesManager()
    
    def __unicode__(self):
        return u"[%s-%s] %s ($%.0f/%s)" % (self.service_category,self.code, self.name,self.price_per_period,self.period)

    def price_per_period_int(self):
        return int(self.price_per_period)

    price_per_period_int = property(price_per_period_int)
    
    
# Models for runtime


class CustomersServices(models.Model):
    quantity = models.IntegerField(verbose_name=_("Cantidad"))
    date_expiration = models.DateField(verbose_name=_("Fecha de vencimiento"))
    
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    objects = CustomersServicesManager()
    
    def get_order_active(self):
        order_related = self.orderitems_customer_service.get_or_none(order__status_id=2)
        if order_related:
            service_name =  order_related
        else:
            service_name = None 
        return service_name

    def service_name(self):
        service = self.get_order_active().service
        if service:
            service_name =  service.service_category.name
        else:
            service_name = None #_(u"Servicio no asignado a ninguna orden")
        return service_name
    
    def service_category(self):
        service = self.get_order_active().service
        if service:
            service_category =  service.service_category
        else:
            service_category = None
        return service_category
    
    def __unicode__(self):
        return u"[%s] %s - %s" % (self.service_name(),self.quantity, self.date_expiration)
    


class Addresses(models.Model):
    country = models.CharField(max_length=300, verbose_name=_(u"País"), null=False, blank=True)
    province = models.CharField(max_length=300, verbose_name=_("Departamento"), null=False, blank=True)
    city = models.CharField(max_length=300, verbose_name=_("Ciudad"), null=False, blank=True)

    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u"%s/%s/%s" % (self.country, self.province, self.city)
    
    
class Customers(models.Model):
    name = models.CharField(max_length=300, verbose_name=_("Nombre"))
    phone = models.CharField(max_length=300, verbose_name=_(u"Teléfono"), null=False, blank=True)
    email = models.CharField(max_length=300, verbose_name=_("Correo"))
 
    address = models.OneToOneField(Addresses, verbose_name=_("Dirección"))
    payment_methods = models.ManyToManyField(PaymentMethods)
    
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.email)
 
 
class CustomerOrders(models.Model):
    status = models.ForeignKey(OrderStatus, related_name='%(class)s_status', verbose_name=_("Estado"))
    customer = models.ForeignKey(Customers, related_name='%(class)s_customer', verbose_name=_("Cliente"))
    
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
 
    def __unicode__(self):
        return u"[%s] %s" % (self.status, self.customer)
 
 
class OrderItems(models.Model):
    order_quantity = models.IntegerField(verbose_name=_("Cantidad"))
    number_of_periods = models.IntegerField(verbose_name=_(u"Número de periodos"))
    discount = models.IntegerField(verbose_name=_("Descuento"))
    
    service = models.ForeignKey(Services, related_name='%(class)s_service', verbose_name=_("Servicio"))
    order = models.ForeignKey(CustomerOrders, related_name='%(class)s_order', verbose_name=_("Orden del cliente"))
    customer_service = models.ForeignKey(CustomersServices, related_name='%(class)s_customer_service', verbose_name=_("Servicio del cliente"))
    
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    objects = OrderItemsManager()
    
    def get_price_per_period(self):
        return int(self.order_quantity*self.service.price_per_period)

    def get_total_price(self):
        return int((self.get_price_per_period()*self.number_of_periods) - self.discount)


    def __unicode__(self):
        return u"%s - %s" % (self.service, self.order)
