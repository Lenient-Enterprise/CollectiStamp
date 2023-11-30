from django.urls import path
from . import views



urlpatterns = [

    path("", views.view_cart, name="view_cart"),
    path("add/<int:product_id>/<int:amount>/", views.add_product, name="add_product"),
    path("decrement/<int:product_id>/<int:amount>/", views.decrement_product, name="decrement_product"),
    path("delete_product/<int:product_id>/", views.delete_product, name="delete_product"),
    path("delete_cart/", views.delete_cart, name="delete_cart"),
]