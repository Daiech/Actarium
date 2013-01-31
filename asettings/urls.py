from django.conf.urls import url, patterns

asettings_urls = patterns('',
    url(r'^billing', 'asettings.views.settings_billing', name='billing'),
    url(r'^organizations', 'asettings.views.settings_organizations', name='organization'),
    url(r'^$', 'account.views.myAccount', name='account'),
)
