from django.contrib import admin
from apps.website.models import *
from django.conf import settings


class OrderedTemplatesAdmin(admin.ModelAdmin):
	list_display = ("user",)
class Tiny_MCE(admin.ModelAdmin):

    class Media:
        js = ('%sjs/vendor/tiny_mce/tiny_mce.js' % settings.STATIC_URL, '%sjs/textareas2.js' % settings.STATIC_URL)


admin.site.register(globalVars)
admin.site.register(feedBack)
admin.site.register(faq, Tiny_MCE)
admin.site.register(OrderedTemplates, OrderedTemplatesAdmin)
admin.site.register(conditions, Tiny_MCE)
admin.site.register(privacy, Tiny_MCE)
