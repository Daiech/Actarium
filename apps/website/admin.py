from django.contrib import admin
from apps.website.models import *
from django.conf import settings


class Tiny_MCE(admin.ModelAdmin):

    class Media:
        js = ('%sjs/vendor/tiny_mce/tiny_mce.js' % settings.STATIC_URL, '%sjs/textareas2.js' % settings.STATIC_URL)


admin.site.register(globalVars)
admin.site.register(feedBack)
admin.site.register(faq)
admin.site.register(OrderedTemplates)
admin.site.register(conditions, Tiny_MCE)
admin.site.register(privacy, Tiny_MCE)
