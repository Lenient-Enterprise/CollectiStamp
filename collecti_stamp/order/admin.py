from django.contrib import admin

from .models import Order, OrderProduct


# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'order_is_finished', 'order_date', 'order_total', 'payment_method', 'delivery_status', 'delivery_method',)
    search_fields = ('user_id',)
    icon_name = 'shopping_cart'


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('quantity',)
    search_fields = ('order_id',)
    icon_name = 'shopping_cart'
