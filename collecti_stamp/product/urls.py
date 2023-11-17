from django.urls import path

from .views import details_product

urlpatterns = [
    path('product/<int:product_id>/', details_product, name='detalle_producto'),
]

