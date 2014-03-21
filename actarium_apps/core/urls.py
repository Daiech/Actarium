from django.conf.urls import url, patterns
from .views import *

customers_services = patterns('',
    url(r'^servicios/(?P<slug_org>[-\w]+)/$', read_organizations_services, name='read_organization_services'),
)


urlpatterns = customers_services