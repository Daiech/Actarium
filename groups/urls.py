from django.conf.urls import url, patterns
groups_urls = patterns('',
    url(r'^new$', 'groups.views.newGroup', name='something'),
    url(r'^(?P<slug_group>[-\w]+)/newMinutes(?P<id_reunion>.*)', 'groups.views.newMinutes', name='something'),
    url(r'^(?P<slug_group>[-\w]+)/newMinutes', 'groups.views.newMinutes', name='something'),
    url(r'^newReunion/(?P<slug>[-\w]+)', 'groups.views.newReunion'),
    url(r'^calendar/(?P<slug>[-\w]*)', 'groups.views.calendarDate'),
    url(r'^calendar', 'groups.views.calendar'),
    url(r'^getMembers$', 'groups.views.getMembers'),
    url(r'^setInvitation$', 'groups.views.newInvitation'),
    url(r'^getReunions$', 'groups.views.getReunions'),
    url(r'^getReunion', 'groups.views.getReunionData'),
    url(r'^setAssistance$', 'groups.views.setAssistance'),
    url(r'^setSign$', 'groups.views.setSign'),
    url(r'^acceptInvitation$', 'groups.views.acceptInvitation'),
    url(r'^deleteInvitation$', 'groups.views.deleteInvitation'),
    url(r'^(?P<slug>[-\w]+)/minutes/(?P<minutes_code>[-\w]+)$', 'groups.views.showMinutes'),
    url(r'^(?P<slug>[-\w]+)', 'groups.views.showGroup'),
    url(r'^$', 'groups.views.groupsList')
)
