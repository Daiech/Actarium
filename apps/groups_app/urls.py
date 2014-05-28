from django.conf.urls import url, patterns

name = "groups"

urlpatterns = patterns('',
    # url(r'^(?P<slug_group>[-\w]+)/admin/emailNotifications', 'apps.emailmodule.views.emailNotifications', name='Email Notifications'),
    url(r'^(?P<slug_group>[-\w]+)/admin/emailAjax', 'apps.emailmodule.views.emailAjax', name='Email Ajax'),
)
urlpatterns += patterns('apps.groups_app.minutes',
    # url(r'^(?P<slug_group>[-\w]+)/roles-for-this-minutes(?P<id_reunion>.*)', 'rolesForMinutes', name='set_role_for_minute'),
    url(r'^(?P<slug_group>[-\w]+)/set-rol-for-minute', 'setRolForMinute', name='Set Role'),
    url(r'^(?P<slug_group>[-\w]+)/set-show-dni', 'setShowDNI', name='Set Show DNI'),
    url(r'^(?P<slug_group>[-\w]+)/add-new-annotation', 'newAnnotation', name='Set annotation'),
    # url(r'^(?P<slug_group>[-\w]+)/create-minutes(?P<id_reunion>.*)/(?P<slug_template>.*)', 'newMinutes', name='New minutes with reunion'),
    url(r'^(?P<slug_group>[-\w]+)/uploadMinutes', 'uploadMinutes', name='uploadMinutes'),
    # url(r'^(?P<slug>[-\w]+)/minutes/(?P<minutes_code>[-\w]+)$', 'showMinutes'),
    # url(r'^(?P<slug_group>[-\w]+)/minutes/(?P<minutes_code>[-\w]+)/edit/(?P<slug_template>.*)$', 'editMinutes'),
    url(r'^uploadMinutesAjax', 'uploadMinutesAjax'),
    url(r'^setApprove$', 'setMinutesApprove'),
    url(r'^(?P<slug_group>[-\w]+)/minutes/create-minutes(?P<id_reunion>.*)/(?P<slug_template>.*)', 'newMinutes', name='create_minutes'),
    url(r'^(?P<slug_group>[-\w]+)/minutes-code/edit/(?P<minutes_code>[-\w.\ ]+)/(?P<slug_template>.*)$', 'editMinutes', name="edit_minutes"),

)
urlpatterns += patterns('apps.groups_app.views',
    # url(r'^(?P<slug_group>[-\w]+)/admin/info', 'groupInfoSettings', name='Admin Info Groups'),
    # url(r'^(?P<slug_group>[-\w]+)/admin/dni', 'groupDNISettings', name='Admin DNI Groups'),
    url(r'^(?P<slug_group>[-\w]+)/admin/request_dni', 'requestDNI', name='Request_DNI_ajax'),
    url(r'^(?P<slug_group>[-\w]+)/admin/resend-invitation', 'resendInvitation', name='Resend_Invitation'),
    url(r'^(?P<slug_group>[-\w]+)/admin/change-names', 'changeNames', name='Change_Names'),
    url(r'^(?P<slug_group>[-\w]+)/admin', 'groupSettings', name='Admin_Groups'),
    url(r'^(?P<slug_group>[-\w]+)/setRole', 'setRole', name='Set_Role'),
    url(r'^(?P<slug_group>[-\w]+)/remove_from_group', 'remove_from_group', name="remove_from_group"),

    # url(r'^newReunion/(?P<slug>[-\w]+)', 'newReunion'),
    url(r'^(?P<slug_group>[-\w]+)/new_reunion$', 'new_reunion', name="new_reunion_group"),
    url(r'^(?P<slug_group>[-\w]+)calendarDate/', 'calendarDate'),
    url(r'^setInvitation$', 'newInvitationToGroup', name="set_invitation"),
    url(r'^getReunions$', 'getReunions'),
    url(r'^getNextReunions$', 'getNextReunions'),
    url(r'^getReunion', 'getReunionData'),
    url(r'^setAssistance$', 'setAssistance'),
    url(r'^acceptInvitation$', 'acceptInvitation'),
    # url(r'^(?P<slug>[-\w]+)$', 'showGroup'),
    url(r'^$', 'groupsList'),
)

urlpatterns += patterns('apps.groups_app.views_groups',
    url(r'^(?P<slug_group>[-\w]+)/config/edit-info$', 'editInfoGroup', name='edit_info_group'),
    url(r'^(?P<slug_group>[-\w]+)/config/email-notifications$', 'configEmailNotifications', name='email_notifications'),
    url(r'^(?P<slug_group>[-\w]+)/config/dni$', 'showGroupDNISettings', name='dni_group'),
    url(r'^(?P<slug_group>[-\w]+)/minutes-code/(?P<minutes_code>[-\w.\ ]+)$', 'showMinuteGroup', name="show_minute"),
    url(r'^(?P<slug_group>[-\w]+)/roles-for-this-minutes(?P<id_reunion>.*)', 'rolesForMinutes', name='set_role_for_minute'),
    url(r'^(?P<slug_group>[-\w]+)/team$', 'showTeamGroup', name="show_team"),
    url(r'^(?P<slug_group>[-\w]+)/folder$', 'showFolderGroup', name="show_folder"),
    url(r'^(?P<slug_group>[-\w]+)/calendar', 'showCalendarGroup', name="show_calendar"),
    url(r'^(?P<slug_group>[-\w]+)/', 'showHomeGroup', name="show_home"),
    url(r'^create$', 'newGeneralGroup', name='new_group'),
)
