from django.conf.urls import url, patterns

asettings_urls = patterns('',
    url(r'^billing', 'asettings.views.settingsBilling', name='billing'),
    url(r'^organizations/new', 'asettings.views.newOrganization', name='New organization'),
    url(r'^organizations', 'asettings.views.settingsOrganizations', name='organization'),
    url(r'^requestPackage', 'asettings.views.requestPackage', name='requestPackage'),
    url(r'^$', 'account.views.myAccount', name='account'),
)
