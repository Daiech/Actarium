from django.conf.urls import patterns, url

name = "account"

urlpatterns = patterns('apps.account.views',
    url(r'^$', 'personalData', name="personal_data"),
    url(r'^new', 'newUser', name="new_user"),
    # url(r'^newInvited', 'newInvitedUser', name="new_invited_user"),
    url(r'^complete-registration', 'complete_registration', name="complete_registration"),
    url(r'^login', 'log_in', name="log_in"),
    url(r'^logout', 'log_out', name="log_out"),
    url(r'^changePassword', 'changePassword', name="change_password"),
    url(r'^dni', 'dni', name="dni"),
    url(r'^set_dni', 'setDNIPermissions', name="set_dni_perms"),
    #url(r'^PasswordRestore', 'PasswordRestore'),
    url(r'^password/reset/$', 'password_reset2', name="password_reset2"),
    url(r'^password/reset/done/$', 'password_reset_done2', name="password_reset_done2"),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm2', name="password_reset_confirm2"),
    #  {'post_reset_redirect' : '/account/password/done/'}),
    url(r'^password/done/$', 'password_reset_complete2', name="password_reset_complete2"),
    url(r'^activate/(?P<activation_key>[-\w]+)/invited(?P<is_invited>.*)', 'confirm_account', name="confirm_account"),
    url(r'^activate/(?P<activation_key>[-\w]+)', 'activate_account', name="activate_account"),
    url(r'^delete-account/', 'delete_account', name="delete_account"),
    url(r'^confirm_account_deleted/', 'confirm_account_deleted', name="confirm_account_deleted"),
    url(r'^list_notifications/', 'list_notifications', name="list_notifications"),
)
