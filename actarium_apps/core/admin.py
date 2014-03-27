from django.contrib import admin


from .models import OrganizationServices, Packages, ServicesRanges, DiscountCodes
admin.site.register(OrganizationServices)
admin.site.register(Packages)
admin.site.register(ServicesRanges)
admin.site.register(DiscountCodes)

