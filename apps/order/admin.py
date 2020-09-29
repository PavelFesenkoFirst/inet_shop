from django.contrib import admin

from apps.order.models import Order, OrderProduct


class OrderAdminInline(admin.TabularInline):
    model = OrderProduct
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderAdminInline,)
