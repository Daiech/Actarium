#encoding:utf-8
from django.db import models

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
    pass
    
class CustomersServicesManager(GenericManager):
    pass

class ServicesManager(GenericManager):
    def get_all_active_orderer(self):
        return self.filter(is_active=True).distinct().order_by('code')