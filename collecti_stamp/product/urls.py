from django.urls import path
from .views import product_details, product_catalog

urlpatterns = [
    path('product/<int:product_id>/', product_details, name='product_details'),
    path('catalog/', product_catalog, name='product_catalog'),
]

