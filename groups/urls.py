from django.conf.urls import patterns #url
groups_urls = patterns('',
    (r'^new$', 'groups.views.newGroup'),
    (r'^newMinutes/(?P<slug>[-\w]+)', 'groups.views.newMinutes'),
    (r'^newReunion/(?P<slug>[-\w]+)', 'groups.views.newReunion'),
    (r'^calendar/(?P<slug>[-\w]*)', 'groups.views.calendarDate'),
    (r'^calendar', 'groups.views.calendar'),
    (r'^getMembers$', 'groups.views.getMembers'),
    (r'^setInvitation$', 'groups.views.newInvitation'),
    (r'^getReunions$', 'groups.views.getReunions'),
    (r'^(?P<slug>[-\w]+)', 'groups.views.showGroup'),
    (r'^$', 'groups.views.groupsList'),
    
)
