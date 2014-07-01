from django.contrib import admin

# Fixtures
from .models import Status, Roles
admin.site.register(Status)
admin.site.register(Roles)

# Runtime
from .models import Tasks, Actions, UserTasks
admin.site.register(Tasks)
admin.site.register(Actions)
admin.site.register(UserTasks)

