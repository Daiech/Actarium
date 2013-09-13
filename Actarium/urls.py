from django.conf.urls import patterns, include, url
from account.urls import account_urls
from groups.urls import groups_urls
from actions_log.urls import actions_log_urls
from asettings.urls import asettings_urls
from pdfmodule.urls import pdfmodule_urls
from billing.urls import billing_urls
from django.conf import settings
from website.views import getGlobalVar

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'website.views.home', name='home'),
    url(r'^about', 'website.views.about'),
    url(r'^help/faq', 'website.views.help'),
    url(r'^feed-back', 'website.views.sendFeedBack'),
    url(r'^' + getGlobalVar("URL_PRIVACY") + '$', 'website.views.privacy_'),
    url(r'^' + getGlobalVar("URL_TERMS") + '$', 'website.views.terms'),

    url(r'^blog', 'website.views.blog'),
    url(r'^update', 'github.views.update'),
    url(r'^runMongo', 'github.views.runMongo'),
    url(r'^account/', include(account_urls)),
    url(r'^groups/', include(groups_urls)),
    url(r'^pdf/', include(pdfmodule_urls)),
    url(r'^actions/', include(actions_log_urls)),
    url(r'^settings/', include(asettings_urls)),
    url(r'^billing/', include(billing_urls)),

    url(r'^ads/(?P<id_ads>[-\w]+)$', 'ads.views.home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^meal/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )
