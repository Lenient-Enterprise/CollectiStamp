from django.urls import path

from .views import ProductDetailsView

urlpatterns = [
    path('product/<int:product_id>/', ProductDetailsView.as_view(), name='product_details'),
]
