from django.conf.urls import url, patterns
from apps.website.views import getGlobalVar


urlpatterns = patterns('apps.website.views',
    url(r'^$', 'home', name='home'),
    url(r'^tour$', 'home', name='tour'),
    url(r'^help/faq$', 'help', name="help"),
    url(r'^feed-back', 'sendFeedBack', name="send_feedback"),
    url(r'^' + getGlobalVar("URL_PRIVACY") + '$', 'privacy_', name="privacy"),
    url(r'^' + getGlobalVar("URL_TERMS") + '$', 'terms', name="terms"),
    url(r'^services.pdf$', 'services', name='services'),
    url(r'^como-funciona$', 'how_it_works', name='how_it_works'),
    url(r'^features.pdf$', 'services', name='features'),
    url(r'^about$', 'benefits', name='benefits'),
    url(r'^about', 'about', name="about"),
    url(r'^pricing', 'pricing', name="pricing"),
    url(r'^blog', 'blog', name="blog"),
    url(r'^landing', 'landing', name="landing"),
    url(r'^users', 'users', name="users"),
    url(r'^fixtures', 'get_initial_data', name="landing"),
    url(r'^quiero-la-plantilla-de-mi-empresa', 'send_template', name="send_template"),
)