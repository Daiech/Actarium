from django.conf.urls import url, patterns

name = "ads"

urlpatterns = patterns('',
    url(r'^(?P<id_ads>[-\w]+)$', 'apps.ads.views.home'),
)