from django.contrib import admin


class OrganizationServicesAdmin(admin.ModelAdmin):
    list_display = ('organization', 'service', 'created', 'is_active')

class PackagesAdmin(admin.ModelAdmin):
	list_display =('code','number_of_members','service','is_active')

class ServicesRangesAdmin(admin.ModelAdmin):
	list_display = ('id','lower', 'upper', 'service')

from .models import OrganizationServices, Packages, ServicesRanges, DiscountCodes, LastMinutesTasks
admin.site.register(OrganizationServices, OrganizationServicesAdmin)
admin.site.register(Packages, PackagesAdmin)
admin.site.register(ServicesRanges,ServicesRangesAdmin)
admin.site.register(DiscountCodes)
admin.site.register(LastMinutesTasks)

