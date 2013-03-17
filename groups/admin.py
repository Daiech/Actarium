from django.contrib import admin

from groups.models import *

admin.site.register(groups)  # aca registramos nuestro modelo con el admin de django
admin.site.register(group_type)
admin.site.register(minutes)
admin.site.register(minutes_type)
admin.site.register(minutes_type_1)
admin.site.register(invitations_groups)
admin.site.register(rel_user_group)
admin.site.register(admin_group)
admin.site.register(rel_user_minutes_assistance)
admin.site.register(rel_user_minutes_signed)
admin.site.register(user_role)
admin.site.register(groups_permissions)
admin.site.register(rel_role_group_permissions)
admin.site.register(packages)
admin.site.register(billing)
admin.site.register(organizations)
admin.site.register(groups_pro)
admin.site.register(rol_user_minutes)
admin.site.register(templates)
admin.site.register(rel_user_private_templates)
admin.site.register(private_templates)
