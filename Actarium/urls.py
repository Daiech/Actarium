from django.conf.urls import patterns, include, url
from account.urls import account_urls
from organization.urls import organization_urls
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'website.views.home', name='home'),
    url(r'^about', 'website.views.about'),
    url(r'^account/', include(account_urls)),
    url(r'^organizations/', include(organization_urls)),
    # url(r'^Actarium/', include('Actarium.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
