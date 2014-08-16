from django.conf.urls import url, patterns
# name = "orgs"
urlpatterns = patterns('actarium_apps.organizations.views',
    
    url(r'^create/', 'createOrg', name="create_org"),
    url(r'^(?P<slug_org>[-\w]+)/$', 'readOrg', name="show_org"), # url(r'^(?P<slug_org>[-\w]+)/edit$', 'updateOrg', name="update_org"),
    url(r'^(?P<slug_org>[-\w]+)/delete$', 'deleteOrg', name="delete_org"),
    
    url(r'^(?P<slug_org>[-\w]+)/settings$', 'settingsOrg', name="profile_org"),
    url(r'^(?P<slug_org>[-\w]+)/team$', 'teamOrg', name="team_org"),
)
    
urlpatterns += patterns('actarium_apps.organizations.views_ajax',
    url(r'^(?P<slug_org>[-\w]+)/get-members$', 'getListMembers', name="get_users_list"),
    url(r'^(?P<slug_org>[-\w]+)/get-groups$', 'get_user_org_groups', name="get_user_org_groups"),
    url(r'^(?P<slug_org>[-\w]+)/change-role$', 'config_admin_to_org', name="config_admin_to_org"),
    url(r'^(?P<slug_org>[-\w]+)/delete-member$', 'delete_member_org', name="delete_member_org"),
    url(r'^(?P<slug_org>[-\w]+)/invite-new-member$', 'set_org_invitation', name="set_org_invitation"),
    url(r'^(?P<slug_org>[-\w]+)/create-invite-new-member$', 'create_invite_user_to_org', name="create_invite_user_to_org"),
)