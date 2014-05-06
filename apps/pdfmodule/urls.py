from django.conf.urls import url, patterns

name = "pdf"

urlpatterns = patterns('apps.pdfmodule.views',
    url(r'^minutestopdf/(?P<id_minutes>[-\w]+)$', 'minutesToPdf', name='minutestopdf'),
    url(r'^minutesHtmltopdf/(?P<html_string>[-\w]+)$', 'minutesHtmlToPdf', name='minutesHtmltopdf'),
    url(r'^(?P<slug_group>[-\w]+)/generate-pdf/$', 'generate_pdf_from_html', name='generate_pdf'),
)
