from django.urls import path
from .views import finish_order, purchase_steps

urlpatterns = [
    path('finish/', finish_order, name='finish_order'),
    path('finish/<int:new_order_id>/', purchase_steps, name='purchase_steps'),
]