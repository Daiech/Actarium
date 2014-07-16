from django.conf.urls import url, patterns

name = "minutes"
namespace = 'minutes'

urlpatterns = patterns('actarium_apps.minutes.ajax',
    url(r'^(?P<slug_group>[-\w]+)/get-commission(?:/(?P<minutes_id>[-\d]+)/)?', 'get_approving_commission', name="get_approving_commission"),
)