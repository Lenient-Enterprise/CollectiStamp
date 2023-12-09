from catalog.views import product_catalog_coins, product_catalog_seals, product_catalog
from django.urls import path

urlpatterns = [
    path('', product_catalog, name='finder'),
    path('coins/', product_catalog_coins, name='product_catalog_coins'),
    path('seals/', product_catalog_seals, name='product_catalog_seals'),
]