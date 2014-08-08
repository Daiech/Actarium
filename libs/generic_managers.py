from django.db import models
from django.contrib.auth.models import UserManager


class GenericManager(models.Manager):

    def get_all_active(self):
        return self.filter(is_active=True).distinct() #.order_by('-modified')

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
        except self.model.MultipleObjectsReturned:
            return None

    def get_active_or_none(self, **kwargs):
        return self.get_or_none(is_active=True, **kwargs)

class CustomUserManager(UserManager):

    def get_all_active(self):
        return self.filter(is_active=True)

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
        except self.model.MultipleObjectsReturned:
            return None

    def get_active_or_none(self, **kwargs):
        return self.get_or_none(is_active=True, **kwargs)
