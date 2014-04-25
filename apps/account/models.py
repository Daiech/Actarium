#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from libs.generic_managers import GenericManager

from hashlib import sha256 as sha_constructor
import random

User.add_to_class('objects', GenericManager())


class ActivationManager(GenericManager):
    """This class is responsible to manage the process of  account activation"""

    def get_activation_key(self, email):
        return sha_constructor(sha_constructor(str(random.random())).hexdigest()[:5] + email).hexdigest()

    def create_key_to_user(self, user):
        if user and user.email:
            return activation_keys.objects.create(id_user=user, activation_key=self.get_activation_key(user.email), email=user.email)
        else:
            return None

class activation_keys(models.Model):
    """
    Table necessary for create an user account, It is used to validate the email.
    """
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    email = models.CharField(max_length=150, verbose_name="Email")
    activation_key = models.CharField(max_length=150, verbose_name="Activation_key")
    date_generated = models.DateTimeField(auto_now=True)
    is_expired = models.BooleanField(default=False)
    
    objects = ActivationManager()

    def __unicode__(self):
        return "%s: %s %s" % (self.email, self.activation_key, self.is_expired)
