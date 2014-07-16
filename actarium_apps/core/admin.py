from django.contrib import admin


class OrganizationServicesAdmin(admin.ModelAdmin):
    list_display = ('organization', 'service', 'created', 'is_active')


from .models import OrganizationServices, Packages, ServicesRanges, DiscountCodes, LastMinutesTasks
admin.site.register(OrganizationServices, OrganizationServicesAdmin)
admin.site.register(Packages)
admin.site.register(ServicesRanges)
admin.site.register(DiscountCodes)
admin.site.register(LastMinutesTasks)

