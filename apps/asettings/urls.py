from django.conf.urls import url, patterns

asettings_urls = patterns('apps.asettings.views',
    url(r'^billing', 'settingsBilling', name='billing'),
    url(r'^templates', 'settingsTemplates', name='templates'),
    url(r'^assignTemplate', 'assignTemplateAjax', name='assign_templates'),
    url(r'^unassignTemplate', 'unassignTemplateAjax', name='unassign_templates'),
    url(r'^organizations/new', 'newOrganization', name='New organization'),
    url(r'^organizations/edit/(?P<id_org>.*)', 'editOrganization', name='Edit organization'),
    url(r'^organizations', 'settingsOrganizations', name='organization'),
    url(r'^requestPackage', 'requestPackage', name='requestPackage'),
    url(r'^replyRequest', 'replyRequestPackage', name='requestPackage'),
    url(r'^setReplyRequest', 'setReplyRequestPackage', name='requestPackage'),
)
asettings_urls += patterns("",
    url(r'^feedback', 'apps.website.views.showFeedBack', name='feedback'),
)
