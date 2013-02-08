from django.conf.urls import url, patterns
groups_urls = patterns('',
    url(r'^new$', 'groups.views.newGroup', name='something'),
    url(r'^(?P<slug_group>[-\w]+)/admin/info', 'groups.views.groupInfoSettings', name='Admin Info Groups'),
    url(r'^(?P<slug_group>[-\w]+)/admin', 'groups.views.groupSettings', name='Admin Groups'),
    url(r'^(?P<slug_group>[-\w]+)/newMinutes(?P<id_reunion>.*)', 'groups.views.newMinutes', name='something'),
    url(r'^(?P<slug_group>[-\w]+)/newMinutes', 'groups.views.newMinutes', name='something'),
    url(r'^newReunion/(?P<slug>[-\w]+)', 'groups.views.newReunion'),
    url(r'^calendar/(?P<slug>[-\w]*)', 'groups.views.calendarDate'),
    url(r'^calendar', 'groups.views.calendar'),
    url(r'^getMembers$', 'groups.views.getMembers'),
    url(r'^setInvitation$', 'groups.views.newInvitation'),
    url(r'^getReunions$', 'groups.views.getReunions'),
    url(r'^getNextReunions$', 'groups.views.getNextReunions'),
    url(r'^getReunion', 'groups.views.getReunionData'),
    url(r'^setAssistance$', 'groups.views.setAssistance'),
    url(r'^setApprove$', 'groups.views.setApprove'),
    url(r'^acceptInvitation$', 'groups.views.acceptInvitation'),
    url(r'^deleteInvitation$', 'groups.views.deleteInvitation'),
    url(r'^(?P<slug>[-\w]+)/minutes/(?P<minutes_code>[-\w]+)$', 'groups.views.showMinutes'),
    url(r'^(?P<slug>[-\w]+)', 'groups.views.showGroup'),
    url(r'^$', 'groups.views.groupsList'),
)
