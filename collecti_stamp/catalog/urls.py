from django.urls import path

from catalog.views import product_catalog

urlpatterns = [
    path('', product_catalog, name='finder'),
    path('catalog/', product_catalog, name='product_catalog'),
]