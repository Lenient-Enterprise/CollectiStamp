from django.urls import path

from .views import details_product, product_catalog

urlpatterns = [
    path('product/<int:product_id>/', details_product, name='detalle_producto'),
    path('catalog/', product_catalog, name='product_catalog'),
]

