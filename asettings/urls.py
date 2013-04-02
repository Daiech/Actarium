from django.conf.urls import url, patterns

asettings_urls = patterns('',
    url(r'^billing', 'asettings.views.settingsBilling', name='billing'),
    url(r'^templates', 'asettings.views.settingsTemplates', name='templates'),
    url(r'^assignTemplate', 'asettings.views.assignTemplateAjax', name='assign_templates'),
    url(r'^unassignTemplate', 'asettings.views.unassignTemplateAjax', name='unassign_templates'),
    url(r'^organizations/new', 'asettings.views.newOrganization', name='New organization'),
    url(r'^organizations/edit/(?P<id_org>.*)', 'asettings.views.editOrganization', name='Edit organization'),
    url(r'^organizations', 'asettings.views.settingsOrganizations', name='organization'),
    url(r'^requestPackage', 'asettings.views.requestPackage', name='requestPackage'),
    url(r'^replyRequest', 'asettings.views.replyRequestPackage', name='requestPackage'),
    url(r'^setReplyRequest', 'asettings.views.setReplyRequestPackage', name='requestPackage'),
    url(r'^$', 'account.views.myAccount', name='account'),
)
