from django.contrib import admin

from .models import rel_user_group

class organizationsAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'description', 'date_added', 'is_active')

admin.site.register(rel_user_group)