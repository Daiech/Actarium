from django.conf.urls import url, patterns
from .views import read_pricing, read_orders

customers_services = patterns('',
    url(r'^pricing/(?P<slug_org>[-\w]+)/$', read_pricing, name='read_pricing'),
    url(r'^admin_orders/$', read_orders, name='admin_orders'),
)


urlpatterns = customers_services