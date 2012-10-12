#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User

class Facebook_data(models.Model):
    usuario         = models.ForeignKey(User)
    fb_username     = models.CharField(max_length=50,unique=True)
    fb_uid          = models.CharField(max_length=50,unique=True)
    first_name      = models.CharField(max_length=60)
    last_name       = models.CharField(max_length=60)
    gender          = models.CharField(max_length=10)
    birthday        = models.DateField()
    location_id     = models.CharField(max_length=100)
    location_name   = models.CharField(max_length=100)
    locale          = models.CharField(max_length=10)
    country         = models.CharField(max_length=10)
    
    def __unicode__(self):
        return self.fb_uid
