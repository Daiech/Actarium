from django.conf.urls import patterns  # , url

account_urls = patterns('',
    (r'^$', 'account.views.myAccount'),
    (r'^new', 'account.views.newUser'),
    (r'^login', 'account.views.log_in'),
    (r'^logout', 'account.views.log_out'),
    (r'^PasswordChange', 'account.views.PasswordChange'),
    #(r'^PasswordRestore', 'account.views.PasswordRestore'),
    (r'^password/reset/$', 'account.views.password_reset2'),
       # {'post_reset_redirect' : '/account/password/reset/done/'}),
    (r'^password/reset/done/$', 'account.views.password_reset_done2'),
    (r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'account.views.password_reset_confirm2'),
          #  {'post_reset_redirect' : '/account/password/done/'}),
    (r'^password/done/$', 'account.views.password_reset_complete2'),
    (r'^activate/(?P<activation_key>[-\w]+)', 'account.views.activate_account'),
)
