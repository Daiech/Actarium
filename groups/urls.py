from django.conf.urls import url, patterns

groups_urls = patterns(
    '',
    url(r'^new$', 'groups.views.newGroup', name='something'),
    url(r'^(?P<slug_group>[-\w]+)/admin/info', 'groups.views.groupInfoSettings', name='Admin Info Groups'),
    url(r'^(?P<slug_group>[-\w]+)/admin', 'groups.views.groupSettings', name='Admin Groups'),
    url(r'^(?P<slug_group>[-\w]+)/roles-for-this-minutes(?P<id_reunion>.*)', 'groups.minutes.rolesForMinutes', name='New minutes with reunion'),
    url(r'^(?P<slug_group>[-\w]+)/setRole', 'groups.views.setRole', name='Set Role'),
    url(r'^(?P<slug_group>[-\w]+)/set-rol-for-minute', 'groups.minutes.setRolForMinute', name='Set Role'),
    url(r'^(?P<slug_group>[-\w]+)/create-minutes(?P<id_reunion>.*)/(?P<slug_template>.*)', 'groups.minutes.newMinutes', name='New minutes with reunion'),
    url(r'^(?P<slug_group>[-\w]+)/uploadMinutes', 'groups.minutes.uploadMinutes', name='uploadMinutes'),
    url(r'^(?P<slug>[-\w]+)/minutes/(?P<minutes_code>[-\w]+)$', 'groups.minutes.showMinutes'),
    url(r'^uploadMinutesAjax', 'groups.minutes.uploadMinutesAjax'),
    url(r'^newReunion/(?P<slug>[-\w]+)', 'groups.views.newReunion'),
    url(r'^calendar/(?P<slug>[-\w]*)', 'groups.views.calendarDate'),
    url(r'^calendar', 'groups.views.calendar'),
    url(r'^getMembers$', 'groups.views.getMembers'),
    url(r'^setInvitation$', 'groups.views.newInvitationToGroup'),
    url(r'^getReunions$', 'groups.views.getReunions'),
    url(r'^getNextReunions$', 'groups.views.getNextReunions'),
    url(r'^getReunion', 'groups.views.getReunionData'),
    url(r'^setAssistance$', 'groups.views.setAssistance'),
    url(r'^setApprove$', 'groups.minutes.setMinutesApprove'),
    url(r'^acceptInvitation$', 'groups.views.acceptInvitation'),
    url(r'^deleteInvitation$', 'groups.views.deleteInvitation'),
    url(r'^(?P<slug>[-\w]+)', 'groups.views.showGroup'),
    url(r'^$', 'groups.views.groupsList'),
)
