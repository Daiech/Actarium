#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User


class actions(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    code = models.CharField(max_length=150, verbose_name="code", unique=True)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "Action: %s " % (self.name)


class rel_user_action(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_action = models.ForeignKey(actions,  null=False, related_name='%(class)s_id_action')
    extra = models.TextField(blank=True)
    date_done = models.DateTimeField(auto_now=True)
