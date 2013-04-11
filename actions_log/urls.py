from django.conf.urls import url, patterns
actions_log_urls = patterns('',
	# url(r'^pdf', 'actions_log.views.getPDF', name='getPDF'),
    url(r'^user/(?P<username>[-\w]+)/order/(?P<field>[-\w]+)$', 'actions_log.views.showUserActionsOrder', name='user_actions_order'),
    url(r'^order/(?P<field>[-\w]+)$', 'actions_log.views.showOrderActions', name='order_actions'),
    url(r'^action/(?P<id_action>[-\w]+)$', 'actions_log.views.showAction', name='order_actions'),
    url(r'^views', 'actions_log.views.showViewsLog', name='views_log'),
    url(r'^(?P<username>[-\w]+)', 'actions_log.views.showUserActions', name='user_actions'),
    url(r'^$', 'actions_log.views.showActions', name='actions'),
   
)
