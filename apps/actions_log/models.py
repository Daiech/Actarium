#encoding:utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class actions(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    code = models.CharField(max_length=150, verbose_name="code", unique=True)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s - %s " % (self.code,self.name)


class rel_user_action(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_action = models.ForeignKey(actions,  null=False, related_name='%(class)s_id_action')
    extra = models.TextField(blank=True)
    date_done = models.DateTimeField(auto_now=True)
    ip_address = models.CharField(max_length=100, verbose_name="IP_address")


class PersonalNotification(models.Model):
    image = models.CharField(max_length=200, verbose_name=_(u"Imagen"))
    message = models.CharField(max_length=200, verbose_name=_(u"Mensaje"))
    url = models.CharField(max_length=200, verbose_name=_(u"Url"))
    user_generator = models.ForeignKey(User,  null=False, related_name='%(class)s_user_generator')
    user_responsible = models.ForeignKey(User,  null=False, related_name='%(class)s_user_responsible')
    type_notification = models.CharField(max_length=200, verbose_name=_(u"Tipo"))
    viewed = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

# class GroupalNotification(models.Model):
#     image = models.CharField(max_length=200, verbose_name=_(u"Imagen"))
#     message = models.CharField(max_length=200, verbose_name=_(u"Mensaje"))
#     url = models.CharField(max_length=200, verbose_name=_(u"Url"))
#     user_generator = models.ForeignKey(User,  null=False, related_name='%(class)s_user_generator')
#     user_responsible = models.ForeignKey(User,  null=False, related_name='%(class)s_user_responsible')
#     type_notification = models.CharField(max_length=200, verbose_name=_(u"Tipo"))
#     viewed = models.BooleanField(default=True)

#     is_active = models.BooleanField(default=True)
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)
