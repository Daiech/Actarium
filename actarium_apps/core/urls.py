from django.conf.urls import url, patterns

customers_services = patterns('actarium_apps.core.views',
    url(r'^servicios$', 'services', name='services'),
)


urlpatterns = customers_services