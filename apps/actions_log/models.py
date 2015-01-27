#encoding:utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from .choices import CHOICE_TYPE_NOTIFICATION, GLYPHICON_CHOICES


class actions(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    code = models.CharField(max_length=150, verbose_name="code", unique=True)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return u"%s - %s " % (self.code,self.name)


class rel_user_action(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_action = models.ForeignKey(actions,  null=False, related_name='%(class)s_id_action')
    extra = models.TextField(blank=True)
    date_done = models.DateTimeField(auto_now=True)
    ip_address = models.CharField(max_length=100, verbose_name="IP_address")


class PersonalNotification(models.Model):
    CHOICE_TYPE_NOTIFICATION = CHOICE_TYPE_NOTIFICATION

    image = models.CharField(max_length=200, verbose_name=_(u"Imagen"))
    message = models.CharField(max_length=400, verbose_name=_(u"Mensaje"))
    url = models.CharField(max_length=400, verbose_name=_(u"Url"))
    user_generator = models.ForeignKey(User,  null=False, related_name='%(class)s_user_generator')
    type_notification = models.CharField(max_length=200, verbose_name=_(u"Tipo"), choices=CHOICE_TYPE_NOTIFICATION)
    

    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%us [%s]"%(self.id, self.type_notification)

    def glyphicon(self):
        return GLYPHICON_CHOICES[self.type_notification]


class UserNotification(models.Model):
    user = models.ForeignKey(User,  null=False, related_name='%(class)s_user_generator')
    personalnotification = models.ForeignKey(PersonalNotification,  null=False, related_name='%(class)s_personalnotification')
    viewed = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s [%s] %s - %s"%(self.id, self.user, self.viewed, self.personalnotification)    