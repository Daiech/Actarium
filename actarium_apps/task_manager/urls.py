from django.conf.urls import url, patterns
from .views import *
from .ajax import *

name = "tasks"
namespace = 'tasks'

urlpatterns = patterns('actarium_apps.task_manager.ajax',
    url(r'^get_minutes_tasks/(?P<minutes_id>[-\w]+)/$', get_minutes_tasks, name='get_minutes_tasks'),
    url(r'^create_task/$', create_task, name='create_task'),
)