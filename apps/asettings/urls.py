from django.conf.urls import url, patterns

name = "settings"

urlpatterns = patterns('apps.asettings.views',
    url(r'^templates', 'settingsTemplates', name='templates'),
    url(r'^assignTemplate', 'assignTemplateAjax', name='assign_templates'),
    url(r'^unassignTemplate', 'unassignTemplateAjax', name='unassign_templates'),
)
urlpatterns += patterns("",
    url(r'^feedback', 'apps.website.views.showFeedBack', name='feedback'),
)
