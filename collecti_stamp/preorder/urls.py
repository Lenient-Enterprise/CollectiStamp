from django.urls import path
from .views import *



urlpatterns = [

    path("", view_cart, name="view_cart"),
    path("add/<int:product_id>/", add_product, name="add_product"),
    path("decrement/<int:product_id>/", decrement_product, name="decrement_product"),
    path("delete_product/<int:product_id>/", delete_product, name="delete_product"),
    path("delete_cart/", delete_cart, name="delete_cart"),
]