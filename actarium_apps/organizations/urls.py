from django.conf.urls import url, patterns

urlpatterns = patterns('actarium_apps.organizations.views',
    url(r'^$', 'listOrgs', name="list_orgs"),
    url(r'^create/', 'createOrg', name="create_org"),
    url(r'^(?P<slug_org>[-\w]+)/$', 'readOrg', name="show_org"), # url(r'^(?P<slug_org>[-\w]+)/edit$', 'updateOrg', name="update_org"),
    url(r'^(?P<slug_org>[-\w]+)/delete$', 'deleteOrg', name="delete_org"),
    
    url(r'^(?P<slug_org>[-\w]+)/profile$', 'profileOrg', name="profile_org"),
    url(r'^(?P<slug_org>[-\w]+)/team$', 'teamOrg', name="team_org"),
)
    
urlpatterns += patterns('actarium_apps.organizations.views_ajax',
    url(r'^(?P<slug_org>[-\w]+)/get-members$', 'getListMembers', name="get_users_list"),
    url(r'^(?P<slug_org>[-\w]+)/change-role$', 'change_role_member_org', name="change_role_member_org"),
)