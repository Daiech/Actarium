from django.contrib import admin

# fixtures
from .models import OrderStatus, Periods
admin.site.register(OrderStatus)
admin.site.register(Periods)

# runtime
from .models import CustomersServices, Addresses, Customers, CustomerOrders, OrderItems
admin.site.register(CustomersServices)
admin.site.register(Addresses)
admin.site.register(Customers)
admin.site.register(CustomerOrders)
admin.site.register(OrderItems)

# Django-Admin
from .models import ServicesCategories, PaymentMethods, Services
admin.site.register(ServicesCategories)
admin.site.register(PaymentMethods)
admin.site.register(Services)

