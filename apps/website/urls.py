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
    url(r'^features.pdf$', 'services', name='features'),
    url(r'^about$', 'benefits', name='benefits'),
    url(r'^about', 'about', name="about"),
    url(r'^pricing', 'pricing', name="pricing"),
    url(r'^blog', 'blog', name="blog"),
    url(r'^landing', 'landing', name="landing"),
)