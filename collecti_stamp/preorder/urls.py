from django.urls import path

from .views import CartView, AddProductView, DecrementProductCartView, DeleteProductCartView, DeleteCartView

urlpatterns = [

    path("", CartView.as_view(), name="view_cart"),
    path("add/<int:product_id>/<int:amount>/",AddProductView.as_view() , name="add_product"),
    path("decrement/<int:product_id>/<int:amount>/",DecrementProductCartView.as_view() , name="decrement_product"),
    path("delete_product/<int:product_id>/",DeleteProductCartView.as_view() , name="delete_product"),
    path("delete_cart/",DeleteCartView.as_view() , name="delete_cart"),
]