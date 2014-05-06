#encoding:utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # to change:
    url(r'^calendar/', 'apps.groups_app.views.calendar', name="calendar"),

    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^oauth/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^meal/', include(admin.site.urls)),
)

for app in settings.APPS:
    try:
        appurls = __import__(app + ".urls", fromlist=['urls'])
        if hasattr(appurls, "name"):
            ns = ""
            if hasattr(appurls, "namespace"):
                ns = appurls.namespace
            urlpatterns += patterns('',
                url(r'^' + appurls.name + '/', include(appurls.urlpatterns, namespace=ns)),
            )
        else:
            urlpatterns += appurls.urlpatterns
    except Exception as e:
        print "Error: ",app, e


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
