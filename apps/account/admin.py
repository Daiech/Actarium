from django.contrib import admin

from apps.account.models import *

admin.site.register(activation_keys)  # aca registramos nuestro modelo con el admin de django
