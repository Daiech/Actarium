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
    due = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    

    def set_task_done(self):
        from .models import UserTasks, Actions, Status, Roles
        from actarium_apps.core.models import LastMinutesTasks
        from django.contrib.auth.models import User

        # validate database configuration - fixtures
        status_obj = Status.objects.get_or_none(code="TER")
        if not (status_obj):
            return False, __(u"Ha ocurrido un error al intentar marcar la tarea como terminada, comunicate con los administradores para solucionarlo")

        if self.status_code == "TER":
            return False, __(u"Esta tarea ya fue marcada como terminada")

        if self.status_code == "NAS":
            return False, __(u"Esta tarea no se puede marcar como terminada")

        responsible_obj = self.responsible
        Actions.objects.create(user=responsible_obj, status=status_obj,task=self)
        return True, __(u"La tarea se ha marcado como terminada")

    def set_task_canceled(self):
        from .models import UserTasks, Actions, Status, Roles
        from actarium_apps.core.models import LastMinutesTasks
        from django.contrib.auth.models import User

        # validate database configuration - fixtures
        status_obj = Status.objects.get_or_none(code="CAN")
        if not (status_obj):
            return False, __(u"Ha ocurrido un error al intentar marcar la tarea como terminada, comunicate con los administradores para solucionarlo")

        if self.status_code == "CAN":
            return False, __(u"Esta tarea ya fue marcada como cancelada")

        if self.status_code == "NAS":
            return False, __(u"Esta tarea no se puede marcar como terminada")

        responsible_obj = self.responsible
        Actions.objects.create(user=responsible_obj, status=status_obj,task=self)
        return True, __(u"La tarea se ha marcado como cancelada")

    def set_task_assigned(self):
        from .models import UserTasks, Actions, Status, Roles
        from actarium_apps.core.models import LastMinutesTasks
        from django.contrib.auth.models import User

        # validate database configuration - fixtures
        status_obj = Status.objects.get_or_none(code="ASI")
        if not (status_obj):
            return False, __(u"Ha ocurrido un error al intentar marcar la tarea como terminada, comunicate con los administradores para solucionarlo")

        if self.status_code == "ASI":
            return False, __(u"Esta tarea ya fue marcada como asignada")

        if self.status_code == "NAS":
            return False, __(u"Esta tarea no se puede marcar como terminada")

        responsible_obj = self.responsible
        Actions.objects.create(user=responsible_obj, status=status_obj,task=self)
        return True, __(u"La tarea se ha marcado como asignada")

    def get_responsible(self):
        return self.usertasks_task.get(role__code="RES").user

    def get_creator(self):
        return self.usertasks_task.get(role__code="CRE").user

    def get_status(self):

        actions = self.actions_task.all().order_by('-created')

        if actions == []:
            return [__(u"Sin asignar"), "#000000"], "NAS"

        action = actions[0]

        
        if action.status.code == "TER":
            return __(u"Terminada"), action.status.color_code, "TER"
        
        
        if action.status.code == "CAN":
            return __(u"Archivada"), action.status.color_code, "CAN"

        
        if action.status.code == "ASI":
            if self.due == None:
                return __(u"Asignada"), action.status.color_code, "ASI"
            days_apart_delta = self.due.date() - datetime.date.today()
            days_apart = days_apart_delta.days
            if days_apart < 0:
                return __(u"Vencida"), "#ff8c8c", "VEN"
            else:
                return __(u"Asignada"), action.status.color_code, "ASI"

        return [__(u"Sin asignar"), "#000000"], "NAS"

        
            
    def get_status_message(self):
        return self.get_status()[0]
        
    def get_status_color(self):
        return self.get_status()[1]

    def get_status_code(self):
        return self.get_status()[2]

    responsible = property(get_responsible)
    creator = property(get_creator)
    status = property(get_status_message)
    color = property(get_status_color)
    status_code = property(get_status_code)
    

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
    
    objects = UserTasksManager()

    def __unicode__(self):
        return u"%s - %s - %s" % (self.task.name,self.user.username,self.role.name)

    def get_minutes(self):
        r = self.task.lastminutestasks_task.first()
        if r:
            return r.minutes
        else:
            return None

    def get_org_name(self):
        m = self.get_minutes()
        if m:
            return m.id_group.organization.name
        else:
            return "Sin Slug"

    def get_group_slug(self):
        mc = self.get_minutes()
        if mc:
            return mc.id_group.slug
        else:
            return "SIn Slug"

    def get_group_name(self):
        mc = self.get_minutes()
        if mc:
            return mc.id_group.name
        else:
            return "No hay Nombre de grupo"


    def get_minutes_code(self):
        mc = self.get_minutes()
        if mc:
            return mc.code
        else:
            print "No hay un LastMinutesTask", self
            return 123
