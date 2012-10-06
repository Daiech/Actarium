from django.conf.urls import patterns #, url
account_urls = patterns('',
    (r'^$', 'account.views.myAccount'),
    (r'^new', 'account.views.newUser'),
    (r'^login', 'account.views.log_in'),
    (r'^logout', 'account.views.log_out'),
)
