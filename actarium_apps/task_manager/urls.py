from django.conf.urls import url, patterns
from .views import *
from .ajax import *

name = "tasks"
namespace = 'tasks'

urlpatterns = patterns('actarium_apps.task_manager.ajax',
    url(r'^get_minutes_tasks/(?P<minutes_id>[-\w]+)/$', get_minutes_tasks, name='get_minutes_tasks'),
    url(r'^create_task/$', create_task, name='create_task'),
    url(r'^set_task_done/$', set_task_done, name='set_task_done'),
    url(r'^set_task_canceled/$', set_task_canceled, name='set_task_canceled'),
    url(r'^get_task/$', get_task, name='get_task'),
    url(r'^delete_task/$', delete_task, name='delete_task'),
)