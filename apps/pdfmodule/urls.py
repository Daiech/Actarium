from django.conf.urls import url, patterns

pdfmodule_urls = patterns('apps.pdfmodule.views',
    url(r'^minutestopdf/(?P<id_minutes>[-\w]+)$', 'minutesToPdf', name='minutestopdf'),
    url(r'^minutesHtmltopdf/(?P<html_string>[-\w]+)$', 'minutesHtmlToPdf', name='minutesHtmltopdf'),
)
