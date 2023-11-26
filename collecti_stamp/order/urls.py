from django.urls import path
from .views import finish_order

urlpatterns = [
    path('finish/', finish_order, name='finish_order'),
]