from django.conf.urls import url, patterns
from .views import read_pricing

customers_services = patterns('',
    url(r'^pricing/(?P<slug_org>[-\w]+)/$', read_pricing, name='read_pricing'),
)


urlpatterns = customers_services