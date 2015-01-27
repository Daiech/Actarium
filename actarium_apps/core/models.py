#encoding:utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import *
# import models
from django.contrib.auth.models import User
from actarium_apps.customers_services.models import Customers, CustomersServices , Services #,  OrderStatus, CustomerOrders, OrderItems
from actarium_apps.organizations.models import Organizations
from actarium_apps.task_manager.models import Tasks
from apps.groups_app.models import minutes as LastMinutes


class ActariumCustomers(models.Model):
    user = models.ForeignKey(User, related_name='%(class)s_user', verbose_name=_("Usuario"))
    customer = models.ForeignKey(Customers, related_name='%(class)s_customer', verbose_name=_("Cliente"))
    
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
 
    objects = ActariumCustomersManager()
    
    def __unicode__(self):
        return u"[%s] %s" % (self.user, self.customer)
    


class OrganizationServices(models.Model):
    organization = models.ForeignKey(Organizations, related_name='%(class)s_organization', verbose_name=_(u"Organización"))
    service = models.ForeignKey(CustomersServices, related_name='%(class)s_service', verbose_name=_("Servicio"))
    
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    objects = OrganizationServicesManager()
 
    def __unicode__(self):
        return u"[%s] %s" % (self.organization, self.service)
    
    
class Packages(models.Model):
    code = models.CharField(max_length=100, verbose_name=_(u"Código"))
    number_of_members = models.CharField(max_length=300, verbose_name=_(u"Número de miembros"))

    service = models.ForeignKey(Services, related_name='%(class)s_service', verbose_name=_("Servicio"))
    
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    objects = PackagesManager()
 
    def __unicode__(self):
        return u"[%s] %s - %s" % (self.code, self.number_of_members, self.service)


class ServicesRanges(models.Model):
    lower = models.IntegerField(verbose_name=_("Limite inferior"))
    upper = models.IntegerField(verbose_name=_("Limite Superior"))
    
    service = models.ForeignKey(Services, related_name='%(class)s_service', verbose_name=_("Servicio"))
    
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    objects = ServicesRangesManager()
 
    def __unicode__(self):
        return u"[%s - %s] %s" % (self.lower, self.upper, self.service)


class DiscountCodes(models.Model):
    code = models.CharField(max_length=100, verbose_name=_(u"Código"))
    value = models.FloatField(verbose_name=_(u"Valor"))
    description = models.TextField(blank=True, verbose_name=_(u"Descripción"))

    user = models.ForeignKey(User, related_name='%(class)s_status', verbose_name=_("Usuario"))
    
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    objects = DiscountCodesManager()
 
    def __unicode__(self):
        return u"%s: $%s" % (self.code, self.value)


class LastMinutesTasks(models.Model):
    minutes = models.ForeignKey(LastMinutes, related_name='%(class)s_minutes', verbose_name=_("Acta"))
    task = models.ForeignKey(Tasks, related_name='%(class)s_task', verbose_name=_("Tarea"))

    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    objects = LastMinutesTasksManager()

    def __unicode__(self):
        return u"%s - %s" % (self.minutes, self.task)