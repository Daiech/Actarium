from django.conf.urls import url, patterns
from .views import *
from .views_ajax import *

customers_services = patterns('',
    url(r'^services/(?P<slug_org>[-\w]+)/$', read_organizations_services, name='read_organization_services'),
    url(r'^get_price/$', get_total_price, name='get_total_price'),
)


urlpatterns = customers_services