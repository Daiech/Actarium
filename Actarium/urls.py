#encoding:utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from apps.account.urls import account_urls
from apps.groups_app.urls import groups_urls
from apps.actions_log.urls import actions_log_urls
from apps.asettings.urls import asettings_urls
from apps.pdfmodule.urls import pdfmodule_urls
from apps.website.views import getGlobalVar

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    ######################################################################################################
    #
    #                                          ¡¡¡¡WARNING!!""
    #      You must to add the first work of you url to the RESERVED_WORDS var in the settings file
    #
    #
    ######################################################################################################
    # Examples:
    url(r'^$', 'apps.website.views.home', name='home'),
    url(r'^tour$', 'apps.website.views.home', name='tour'),
    # url(r'^about', 'apps.website.views.about'),
    url(r'^help/faq', 'apps.website.views.help'),
    url(r'^feed-back', 'apps.website.views.sendFeedBack'),
    url(r'^' + getGlobalVar("URL_PRIVACY") + '$', 'apps.website.views.privacy_'),
    url(r'^' + getGlobalVar("URL_TERMS") + '$', 'apps.website.views.terms'),

    url(r'^blog', 'apps.website.views.blog'),
    url(r'^update', 'apps.github.views.update'),
    url(r'^runMongo', 'apps.github.views.runMongo'),
    url(r'^account/', include(account_urls)),
    url(r'^groups/', include(groups_urls)),
    url(r'^pdf/', include(pdfmodule_urls)),
    url(r'^actions/', include(actions_log_urls)),
    url(r'^settings/', include(asettings_urls)),
    url(r'^calendar/', 'apps.groups_app.views.calendar', name="calendar"),
    url(r'^email/$', 'apps.emailmodule.views.show_template'),

    url(r'^ads/(?P<id_ads>[-\w]+)$', 'apps.ads.views.home'),
    url(r'^services.pdf$', 'apps.website.views.services', name='services'),
    url(r'^features.pdf$', 'apps.website.views.services', name='features'),
    url(r'^about$', 'apps.website.views.benefits', name='benefits'),

    url(r'^actarium/', include('actarium_apps.core.urls', namespace='core')),
    url(r'^services/', include('actarium_apps.customers_services.urls', namespace='services')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^oauth/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^meal/', include(admin.site.urls)),
    url(r'^', include('actarium_apps.organizations.urls')),

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
