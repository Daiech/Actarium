from django.conf.urls import url, patterns

#Urls to new group design

groups_urls = patterns(
    '',
    url(r'^new$', 'groups.views.newGroup', name='something'),
    url(r'^(?P<slug_group>[-\w]+)/minutes/(?P<minutes_code>[-\w]+)/edit/(?P<slug_template>.*)$', 'groups.minutes.editMinutes'),
    url(r'^(?P<slug_group>[-\w]+)/admin/info', 'groups.views.groupInfoSettings', name='Admin Info Groups'),
    url(r'^(?P<slug_group>[-\w]+)/admin/dni', 'groups.views.groupDNISettings', name='Admin DNI Groups'),
    url(r'^(?P<slug_group>[-\w]+)/admin/request_dni', 'groups.views.requestDNI', name='Request DNI ajax'),
    url(r'^(?P<slug_group>[-\w]+)/admin/resend-invitation', 'groups.views.resendInvitation', name='Resend Invitation'),
    url(r'^(?P<slug_group>[-\w]+)/admin/change-names', 'groups.views.changeNames', name='Change Names'),
    url(r'^(?P<slug_group>[-\w]+)/admin/emailNotifications', 'emailmodule.views.emailNotifications', name='Email Notifications'),
    url(r'^(?P<slug_group>[-\w]+)/admin/emailAjax', 'emailmodule.views.emailAjax', name='Email Ajax'),
    url(r'^(?P<slug_group>[-\w]+)/admin', 'groups.views.groupSettings', name='Admin Groups'),
    url(r'^(?P<slug_group>[-\w]+)/roles-for-this-minutes(?P<id_reunion>.*)', 'groups.minutes.rolesForMinutes', name='New minutes with reunion'),
    url(r'^(?P<slug_group>[-\w]+)/setRole', 'groups.views.setRole', name='Set Role'),
    url(r'^(?P<slug_group>[-\w]+)/set-rol-for-minute', 'groups.minutes.setRolForMinute', name='Set Role'),
    url(r'^(?P<slug_group>[-\w]+)/set-show-dni', 'groups.minutes.setShowDNI', name='Set Show DNI'),
    url(r'^(?P<slug_group>[-\w]+)/add-new-annotation', 'groups.minutes.newAnnotation', name='Set annotation'),
    url(r'^(?P<slug_group>[-\w]+)/create-minutes(?P<id_reunion>.*)/(?P<slug_template>.*)', 'groups.minutes.newMinutes', name='New minutes with reunion'),
    url(r'^(?P<slug_group>[-\w]+)/uploadMinutes', 'groups.minutes.uploadMinutes', name='uploadMinutes'),
    # url(r'^(?P<slug>[-\w]+)/minutes/(?P<minutes_code>[-\w]+)$', 'groups.minutes.showMinutes'),
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
    url(r'^(?P<slug_group>[-\w]+)/deleteInvitation$', 'groups.views.deleteInvitation'),
    # url(r'^(?P<slug>[-\w]+)$', 'groups.views.showGroup'),
    url(r'^$', 'groups.views.groupsList'),
)

groups_urls += patterns('groups.views_groups',
    url(r'^(?P<slug_group>[-\w]+)/minutes/(?P<minutes_code>[-\w]+)$', 'showMinuteGroup', name="show_minute"),
    url(r'^(?P<slug_group>[-\w]+)/team$', 'showTeamGroup', name="show_team"),
    url(r'^(?P<slug_group>[-\w]+)/folder$', 'showFolderGroup', name="show_folder"),
    url(r'^(?P<slug_group>[-\w]+)/calendar$', 'showCalendarGroup', name="show_calendar"),
    url(r'^(?P<slug_group>[-\w]+)/', 'showHomeGroup', name="show_home"),
)