from django.conf.urls import patterns, include, url
from account.urls import account_urls
from groups.urls import groups_urls
from actions_log.urls import actions_log_urls
from asettings.urls import asettings_urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'website.views.home', name='home'),
    url(r'^about', 'website.views.about'),
    url(r'^feed-back', 'website.views.sendFeedBack'),
    url(r'^update', 'github.views.update'),
    url(r'^account/', include(account_urls)),
    url(r'^groups/', include(groups_urls)),
    url(r'^actions/', include(actions_log_urls)),
    url(r'^settings/', include(asettings_urls)),
    # url(r'^Actarium/', include('Actarium.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
