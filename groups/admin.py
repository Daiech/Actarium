from django.contrib import admin

from groups.models import *

admin.site.register(groups)  # aca registramos nuestro modelo con el admin de django
admin.site.register(group_type)
admin.site.register(minutes)
admin.site.register(minutes_type)
admin.site.register(minutes_type_1)
admin.site.register(invitations)
admin.site.register(rel_user_group)
admin.site.register(admin_group)
admin.site.register(rel_user_minutes_assistance)
admin.site.register(user_role)
admin.site.register(groups_permissions)
admin.site.register(rel_role_group_permissions)
admin.site.register(packages)
admin.site.register(billing)

