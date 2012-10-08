#encoding:utf-8
from django.db import models
from django.template import defaultfilters
from django.contrib.auth.models import User

class organizations(models.Model):
    name = models.CharField(max_length = 60, verbose_name="name")
    id_creator = models.ForeignKey(User)
    date_joined = models.DateTimeField()
    description = models.TextField(blank = True)
    is_active = models.BooleanField()
    
    def __unicode__(self):
        return "%s "%(self.name)
    


