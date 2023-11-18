from django.urls import path

from .views import product_details

urlpatterns = [
    path('product/<int:product_id>/', product_details, name='product_details'),
]

