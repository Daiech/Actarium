from django.conf.urls import url, patterns
pdfmodule_urls = patterns('',
    url(r'^minutestopdf/(?P<id_minutes>[-\w]+)$', 'pdfmodule.views.minutesToPdf', name='minutestopdf'),
    url(r'^minutesHtmltopdf/(?P<html_string>[-\w]+)$', 'pdfmodule.views.minutesHtmlToPdf', name='minutesHtmltopdf'),
)
