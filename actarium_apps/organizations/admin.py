from django.contrib import admin

from .models import Organizations, Groups, rel_user_group, OrganizationsUser, OrganizationsRoles

class OrganizationsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'date_added', 'is_archived', 'is_active')

class OrganizationsUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'organization', 'date_added','date_modified', 'is_active')

class RelUserGroupAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'id_user_invited', 'id_group', 'is_member', 'is_admin', 'is_secretary', 'is_superadmin', 'is_convener', 'is_active')

admin.site.register(Organizations, OrganizationsAdmin)
# admin.site.register(Groups)
admin.site.register(rel_user_group, RelUserGroupAdmin)
admin.site.register(OrganizationsRoles)
admin.site.register(OrganizationsUser, OrganizationsUserAdmin)