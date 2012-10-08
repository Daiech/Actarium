from django.conf.urls import patterns #, url
organization_urls = patterns('',
    (r'^$', 'organization.views.list'),
    (r'^new', 'organization.views.new'),
)
