#encoding:utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _



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
    
    def get_due_tasks_by_user(self):
        pass

    def get_tasks_by_user(self):
        pass

    def get_tasks_done_by_user(self):
        pass

    def get_tasks_cancelled_by_user(self):
        pass

    def get_tasks_by_minutes(self, minutes_id):
        tasks_list = self.filter(lastminutestasks_task__minutes_id=minutes_id).order_by('-modified')
        return tasks_list

    def get_tasks_by_group(self):
        pass

