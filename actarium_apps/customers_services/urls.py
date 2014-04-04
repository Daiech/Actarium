from django.conf.urls import url, patterns
from .views import read_pricing, read_orders
from .views_ajax import approve_order

customers_services = patterns('',
    url(r'^pricing/(?P<slug_org>[-\w]+)/$', read_pricing, name='read_pricing'),
    url(r'^admin_orders/$', read_orders, name='admin_orders'),
    url(r'^approve_order/$', approve_order, name='approve_order'),
)


urlpatterns = customers_services