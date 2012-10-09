#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User

class Groups(models.Model):
    
    def __unicode__(self):
        return self.fb_uid
