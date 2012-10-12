from django.conf.urls import patterns #, url
groups_urls = patterns('',
    (r'^new', 'groups.views.newGroup'),
    (r'^(?P<slug>[-\w]+)', 'groups.views.showGroup'),
    (r'^$', 'groups.views.groupsList'),
)