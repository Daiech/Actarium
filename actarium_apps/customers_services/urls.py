from django.conf.urls import url, patterns
from .views import read_pricing

customers_services = patterns('',
    url(r'^precios$', read_pricing, name='read_pricing'),
)


urlpatterns = customers_services