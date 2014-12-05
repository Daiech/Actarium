from django.conf.urls import url, patterns

name = "actions"

urlpatterns = patterns('apps.actions_log.ajax', 
	 url(r'^update_notification$', 'update_notification', name='update_notification'),
)

urlpatterns += patterns('apps.actions_log.views',
	# url(r'^pdf', 'getPDF', name='getPDF'),
    url(r'^user/(?P<username>[-\w]+)/order/(?P<field>[-\w]+)$', 'showUserActionsOrder', name='user_actions_order'),
    url(r'^order/(?P<field>[-\w]+)$', 'showOrderActions', name='order_actions'),
    url(r'^action/(?P<id_action>[-\w]+)$', 'showAction', name='order_actions'),
    url(r'^views$', 'showViewsLog', name='views_log'),
    url(r'^viewsstats$', 'showViewsStats', name='views_stats'),
    url(r'^(?P<username>[-\w.@ ]+)', 'showUserActions', name='user_actions'),
    url(r'^$', 'showActions', name='actions'),
   
)

