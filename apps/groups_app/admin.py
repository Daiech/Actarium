from django.contrib import admin

from apps.groups_app.models import *


class minutesAdmin(admin.ModelAdmin):
    list_display = ('code', 'id_group', 'minutesIsFullSigned', 'minutesIsValid')


class GroupsAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_added', 'is_active')


class billingAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'id_package', 'date_request', 'groups_pro_available', 'date_start', 'date_end', 'state')


class packagesAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_groups_pro', 'price', 'is_visible', 'date_joined', 'time')


class privateTemplatesAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'id_template', 'date_joined')


class organizationsAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'description', 'date_added', 'is_active')


class groupsProAdmin(admin.ModelAdmin):
    list_display = ('id_group', 'id_organization', 'id_billing', 'is_active', 'dateOff')


class DNI_typeAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'long_name')


admin.site.register(Groups, GroupsAdmin)  # aca registramos nuestro modelo con el admin de django
admin.site.register(minutes, minutesAdmin)
admin.site.register(packages, packagesAdmin)
admin.site.register(billing, billingAdmin)
admin.site.register(Organizations, organizationsAdmin)
admin.site.register(private_templates, privateTemplatesAdmin)
admin.site.register(DNI_type, DNI_typeAdmin)
admin.site.register(minutes_type)
admin.site.register(minutes_type_1)
admin.site.register(reunions)
admin.site.register(invitations_groups)
admin.site.register(rel_user_group)
admin.site.register(rel_user_minutes_assistance)
admin.site.register(rel_user_minutes_signed)
admin.site.register(user_role)
admin.site.register(groups_permissions)
admin.site.register(rel_role_group_permissions)
admin.site.register(groups_pro, groupsProAdmin)
admin.site.register(rol_user_minutes)
admin.site.register(templates)
admin.site.register(rel_user_private_templates)
admin.site.register(annotations)
admin.site.register(annotations_comments)
admin.site.register(minutes_version)
admin.site.register(minutes_approver_version)
