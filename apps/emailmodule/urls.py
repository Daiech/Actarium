from django.conf.urls import url, patterns

name = "email"

urlpatterns = patterns('',
	url(r'^$', 'apps.emailmodule.views.show_template'),
)