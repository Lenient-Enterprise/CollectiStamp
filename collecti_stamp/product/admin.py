from django.contrib import admin

from .models import Product
from .models import Criteria

@admin.register(Criteria)
class CriteriaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    icon_name = 'style'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock_amount', 'product_type', 'category')
    search_fields = ('name',)
    icon_name = 'shopping_cart'