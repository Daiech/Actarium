from django.conf.urls import url, patterns
from .views import *
from .views_ajax import *

name = "actarium"
namespace = 'core'

urlpatterns = patterns('',
    url(r'^services/(?P<slug_org>[-\w]+)/$', read_organization_services, name='read_organization_services'),
    url(r'^get_price/$', get_total_price, name='get_total_price'),
    url(r'^get_discount_value/$', get_discount_value, name='get_discount_value'),
    url(r'^search_minutes/$', search_minutes, name='search_minutes'),
)