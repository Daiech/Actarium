from django.conf.urls import patterns #, url
groups_urls = patterns('',
    (r'^$', 'groups.views.list'),
    (r'^new', 'groups.views.new'),
    (r'^minutes', 'groups.views.listMinutes'),
)
