from django.contrib import admin

from .models import Order, OrderProduct


# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_is_finished', 'order_date', 'order_total', 'payment_method', 'delivery_status', 'delivery_method',)
    search_fields = ('id',)
    icon_name = 'shopping_cart'

