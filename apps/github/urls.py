from django.conf.urls import url, patterns

name = ""

urlpatterns = patterns('apps.github.views',
    url(r'^update$', 'update', name="update"),
    url(r'^runMongo$', 'runMongo', name="mongo"),
)