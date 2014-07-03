#encoding:utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import datetime

from .managers import *


class Roles(models.Model):
    code = models.CharField(max_length=300, verbose_name=_(u"Código"))
    name = models.CharField(max_length=300, verbose_name=_("Nombre"))
    description = models.TextField(blank=True, verbose_name=_(u"Descripción"))
    is_active = models.BooleanField(default=True)
    
    objects = GenericManager()

    def __unicode__(self):
        return u"[%s] %s" % (self.code,self.name)


class Status(models.Model):
    code = models.CharField(max_length=300, verbose_name=_(u"Código"))
    name = models.CharField(max_length=300, verbose_name=_("Nombre"))
    description = models.TextField(blank=True, verbose_name=_(u"Descripción"))
    color_code = models.CharField(max_length=20, verbose_name=_(u"Color"))
    is_active = models.BooleanField(default=True)
    
    objects = GenericManager()
    
    def __unicode__(self):
        return u"[%s] %s" % (self.code,self.name)

class Tasks(models.Model):
    name = models.CharField(max_length=300, verbose_name=_("Nombre"))
    description = models.TextField(blank=True, verbose_name=_(u"Descripción"))
    due = models.DateTimeField()

    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def create_task(self):
        pass

    def update_task(self):
        pass

    def delete_task(self):
        pass

    def set_task_done(self):
        pass

    def set_task_canceled(self):
        pass

    def get_responsible(self):
        return self.usertasks_task.get(role__code="RES").user

    def get_color(self):

        action = self.actions_task.get_or_none(status__code="TER")
        if action != None:
            return action.status.color_code
        
        action = self.actions_task.get_or_none(status__code="CAN")
        if action != None:
            return action.status.color_code

        action = self.actions_task.get_or_none(status__code="ASI")
        if action != None:
            days_apart_delta = self.due.date() - datetime.date.today()
            days_apart = days_apart_delta.days
            if days_apart < 0:
                return "#ff8c8c"
            else:
                return action.status.color_code

        return "#000000"

        return color

            

    responsible = property(get_responsible)
    color = property(get_color)


    objects = TasksManager()

    def __unicode__(self):
        return u"%s" % (self.name)

class Actions(models.Model):
    user = models.ForeignKey(User, related_name='%(class)s_user', verbose_name=_("Usuario"))
    status = models.ForeignKey(Status, related_name='%(class)s_status', verbose_name=_("Estado"))
    task = models.ForeignKey(Tasks, related_name='%(class)s_task', verbose_name=_("Tarea"))

    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    objects = GenericManager()

    def __unicode__(self):
        return u"%s - %s - %s" % (self.task.name,self.user.username,self.status.name)


class UserTasks(models.Model):
    user = models.ForeignKey(User, related_name='%(class)s_user', verbose_name=_("Usuario"))
    role = models.ForeignKey(Roles, related_name='%(class)s_role', verbose_name=_("Rol"))
    task = models.ForeignKey(Tasks, related_name='%(class)s_task', verbose_name=_("Tarea"))

    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    objects = GenericManager()

    def __unicode__(self):
        return u"%s - %s - %s" % (self.task.name,self.user.username,self.role.name)