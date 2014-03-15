#encoding:utf-8
from django.db import models

class OrderItemsManager(models.Manager):

    def service_name(self):
        return "nombre del servicio"
    
class CustomersServicesManager(models.Manager):
    
    def service_name(self):
        return " nombre servicio customerService"