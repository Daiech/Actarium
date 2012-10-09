from django.conf.urls import patterns #, url
groups_urls = patterns('',
    (r'^$', 'groups.views.groupsList'),
    (r'^new', 'groups.views.newGroup'),
    (r'^minutes', 'groups.views.minutesList'),
)
