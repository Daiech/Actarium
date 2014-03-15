#encoding:utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import *
# import models
from django.contrib.auth.models import User
from actarium_apps.customers_services.models import Customers, CustomersServices
from actarium_apps.organizations.models import Organizations


class ActariumCustomers(models.Model):
    user = models.ForeignKey(User, related_name='%(class)s_status', verbose_name=_("Usuario"))
    customer = models.ForeignKey(Customers, related_name='%(class)s_customer', verbose_name=_("Cliente"))
    
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
 
    def __unicode__(self):
        return u"[%s] %s" % (self.user, self.customer)
    


class OrganizationServices(models.Model):
    organization = models.ForeignKey(Organizations, related_name='%(class)s_organization', verbose_name=_("Organizacion"))
    service = models.ForeignKey(CustomersServices, related_name='%(class)s_service', verbose_name=_("Servicio"))
    
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
 
    def __unicode__(self):
        return u"[%s] %s" % (self.organization, self.service)
    
    objects = OrganizationServicesManager()