#encoding:utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __



class GenericManager(models.Manager):

    def get_all_active(self):
        return self.filter(is_active=True).distinct().order_by('-modified')

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
        except self.model.MultipleObjectsReturned:
            return None

    def get_active_or_none(self, **kwargs):
        return self.get_or_none(is_active=True, **kwargs)


class TasksManager(GenericManager):
    
    def create_task(self, name, description, responsible_obj, due, minutes_obj, user_obj):
        from .models import UserTasks, Actions, Status, Roles
        from actarium_apps.core.models import LastMinutesTasks
        from django.contrib.auth.models import User

        if description is None:
            description = ""
        # validate database configuration - fixtures
        status_obj = Status.objects.get_or_none(code="ASI")
        creator_role_obj = Roles.objects.get_or_none(code="CRE")
        responsible_role_obj = Roles.objects.get_or_none(code="RES")
        if not (status_obj and creator_role_obj and responsible_role_obj):
            return None , _(u"Existe un problema al intentar aplicar los roles")

        task_obj = self.create(name=name,description=description,due=due)
        UserTasks.objects.create(user=user_obj,role=creator_role_obj,task=task_obj)
        

        UserTasks.objects.create(user=responsible_obj,role=responsible_role_obj,task=task_obj)
        Actions.objects.create(user=responsible_obj, status=status_obj,task=task_obj)
        LastMinutesTasks.objects.create(minutes= minutes_obj,task=task_obj)


        return task_obj, __(u"Tarea creada correctamente en el acta: ")+minutes_obj.code

    def update_task(self, name, description, responsible_obj, due, minutes_obj, user_obj, task_id):
        task_obj = self.get_or_none(id=task_id)
        if task_obj == None:
            return None,  __(u"La tarea que desea modificar no existe")

        if not (task_obj.creator == user_obj):
            return None, __( u"No puedes modificar una tarea creada por otro usuario" )
            

        if task_obj.status_code in ("TER", "CAN", "NAS"):
            return None, __( u"Esta tarea ya no se puede modificar" )

        task_obj.name = name
        print "Actualizando ",description
        if task_obj.description != description:
            task_obj.description = description
        
        usertask_obj =  task_obj.usertasks_task.get(role__code="RES")
        usertask_obj.user= responsible_obj
        usertask_obj.save()
        task_obj.due = due

        task_obj.save()

        return task_obj, __(u"La tarea ha sido actualizada correctamente")
        
    def delete_task(self,task_id, user_obj):

        # verify if task exist
        task_obj = self.get_or_none(id=task_id)
        if not task_obj:
            return None, __( u"No existe esta tarea" )
            

        # owner verification
        if not (task_obj.creator == user_obj):
            return None, __( u"No puedes eliminar una tarea creada por otro usuario" )
            
        if task_obj.status_code in ("TER", "CAN", "NAS"):
            return None, __( u"Esta tarea ya no se puede eliminar" )

        task_obj.is_active = False
        task_obj.save()

        return task_obj, __(u"La tarea ha sido eliminada")


    def get_due_tasks_by_user(self):
        pass

    def get_tasks_by_user(self):
        pass

    def get_tasks_done_by_user(self):
        pass

    def get_tasks_cancelled_by_user(self):
        pass

    def get_tasks_by_minutes(self, minutes_id):
        tasks_list = self.filter(lastminutestasks_task__minutes_id=minutes_id, is_active=True).order_by('-modified')
        return tasks_list

    def get_tasks_by_group(self):
        pass



class UserTasksManager(GenericManager):

    def get_pending_tasks_by_user(self,user):

        usertasks = self.filter(user=user, role__code="RES").order_by('-created')
        tasks_excluded = []
        for usertask in usertasks:
            if usertask.task.status_code == 'TER':
                tasks_excluded.append(usertask.id)
        usertasks = usertasks.exclude(id__in=tasks_excluded)

        return usertasks