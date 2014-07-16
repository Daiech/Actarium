from django.contrib import admin

class CustomerOrdersAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status', 'is_active')

class CustomersServicesAdmin(admin.ModelAdmin):
    list_display = ('quantity', 'date_expiration', 'created', 'is_active')

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order_quantity', 'number_of_periods', 'discount', 'service', 'order', 'customer_service', 'is_active')

class ServicesAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'price_per_period', 'period', 'is_active')


# fixtures
from .models import OrderStatus, Periods
admin.site.register(OrderStatus)
admin.site.register(Periods)

# runtime
from .models import CustomersServices, Addresses, Customers, CustomerOrders, OrderItems
admin.site.register(CustomersServices, CustomersServicesAdmin)
admin.site.register(Addresses)
admin.site.register(Customers)
admin.site.register(CustomerOrders, CustomerOrdersAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)

# Django-Admin
from .models import ServicesCategories, PaymentMethods, Services
admin.site.register(ServicesCategories)
admin.site.register(PaymentMethods)
admin.site.register(Services, ServicesAdmin)

