from django.contrib import admin

from apps.billing.models import *


admin.site.register(Billing)
# admin.site.register(PaymentMethod)
admin.site.register(Order)
# admin.site.register(OrderStatus)
admin.site.register(OrderCustomization)
admin.site.register(OrderTeamSize)
# admin.site.register(Timetable)
admin.site.register(OrderAdvertising)
# admin.site.register(PriceCustomization)
# admin.site.register(PriceTeamSize)
# admin.site.register(PriceAdvertising)
admin.site.register(RelCustomizationOrderExp)
admin.site.register(RelTeamSizeOrderExp)
admin.site.register(RelAdvertisingOrderExp)
admin.site.register(ExpCustomization)
admin.site.register(ExpTeamSize)
admin.site.register(ExpAdvertising)
admin.site.register(Advertising)
admin.site.register(AdvertisingLog)
admin.site.register(AdvertisingLogType)
