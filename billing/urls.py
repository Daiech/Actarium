from django.conf.urls import url, patterns

billing_urls = patterns('billing.views',
    url(r'^to_order', 'to_order', name='to_order'),
    url(r'^my_products', 'my_products', name='my_products'),
    url(r'^billing_history', 'billing_history', name='billing_history'),
    url(r'^get_advertising', 'get_advertising', name='get_advertising'),
    url(r'^create_advertising', 'create_advertising', name='create_advertising'),
    url(r'^show_advertising_stats', 'show_advertising_stats', name='show_advertising_stats'),
    url(r'^random_advertising', 'random_advertising', name='random_advertising'),
)
