from django.contrib import admin

from groups.models import groups,group_type

admin.site.register(groups)  # aca registramos nuestro modelo con el admin de django
admin.site.register(group_type)
