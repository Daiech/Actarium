from django.conf.urls import patterns #url
groups_urls = patterns('',
    (r'^new$', 'groups.views.newGroup'),
    (r'^newMinutes/(?P<slug>[-\w]+)', 'groups.views.newMinutes'),
    (r'^newReunion/(?P<slug>[-\w]+)', 'groups.views.newReunion'),
    (r'^getMembers$', 'groups.views.getMembers'),
    (r'^setInvitation$', 'groups.views.newInvitation'),
    (r'^(?P<slug>[-\w]+)', 'groups.views.showGroup'),
    (r'^$', 'groups.views.groupsList'),
    
)
