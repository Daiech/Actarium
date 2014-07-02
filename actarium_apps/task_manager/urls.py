from django.conf.urls import url, patterns
from .views import *
from .ajax import *

name = "tasks"
namespace = 'tasks'

urlpatterns = patterns('actarium_apps.task_manager.ajax',
    url(r'^get_minutes_tasks/(?P<minutes_id>[-\w]+)/$', get_minutes_tasks, name='get_minutes_tasks'),
    # url(r'^get_price/$', get_total_price, name='get_total_price'),
    # url(r'^get_discount_value/$', get_discount_value, name='get_discount_value'),
)