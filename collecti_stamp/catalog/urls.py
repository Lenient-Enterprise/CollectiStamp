from django.urls import path

from catalog.views import filter_product

urlpatterns = [
    path('', filter_product, name='finder'),
]