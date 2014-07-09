#encoding:utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __
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

    def get_status(self):

        action = self.actions_task.get_or_none(status__code="TER")
        if action != None:
            return __(u"Terminada"), action.status.color_code
        
        action = self.actions_task.get_or_none(status__code="CAN")
        if action != None:
            return __(u"Cancelada"), action.status.color_code

        action = self.actions_task.get_or_none(status__code="ASI")
        if action != None:
            days_apart_delta = self.due.date() - datetime.date.today()
            days_apart = days_apart_delta.days
            if days_apart < 0:
                return __(u"Vencida"), "#ff8c8c"
            else:
                return __(u"Asignada"), action.status.color_code

        return [__(u"Sin asignar"), "#000000"]
            
    def get_status_message(self):
        return self.get_status()[0]
        
    def get_status_color(self):
        return self.get_status()[1]

    responsible = property(get_responsible)
    status = property(get_status_message)
    color = property(get_status_color)
    

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