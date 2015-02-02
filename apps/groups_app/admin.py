from django.contrib import admin

from apps.groups_app.models import *


class minutesAdmin(admin.ModelAdmin):
    list_display = ('code', 'id_group', 'minutesIsFullSigned', 'minutesIsValid')


class GroupsAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_added', 'is_active')


class privateTemplatesAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'id_group', 'id_template', 'date_joined')


class DNI_typeAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'long_name')

class rol_user_minutesAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'id_group', 'id_minutes',"is_president","is_secretary","is_approver","is_assistant","is_signer", 'is_active')


class rel_user_minutes_signedAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'id_minutes', "is_signed_approved")

class rel_user_minutes_assistanceAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'id_minutes', "assistance", "date_assistance")

class TemplatesAdmin(admin.ModelAdmin):
    list_display = ('name', 'address_template', 'show_logo', 'is_public', "date_joined")
    prepopulated_fields = {'slug': ('name',), }

class rel_user_private_templatesAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'id_template', "date_joined")


admin.site.register(Groups, GroupsAdmin)  # aca registramos nuestro modelo con el admin de django
admin.site.register(minutes, minutesAdmin)
admin.site.register(DNI_type, DNI_typeAdmin)
admin.site.register(minutes_type)
admin.site.register(minutes_type_1)
admin.site.register(reunions)
admin.site.register(rel_user_minutes_assistance, rel_user_minutes_assistanceAdmin)
admin.site.register(rel_user_minutes_signed, rel_user_minutes_signedAdmin)
admin.site.register(rol_user_minutes, rol_user_minutesAdmin)
admin.site.register(templates, TemplatesAdmin)
admin.site.register(rel_user_private_templates, rel_user_private_templatesAdmin)
admin.site.register(private_templates, privateTemplatesAdmin)
admin.site.register(annotations)
admin.site.register(annotations_comments)
admin.site.register(minutes_version)
admin.site.register(minutes_approver_version)

