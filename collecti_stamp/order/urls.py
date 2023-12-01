from django.urls import path
from .views import finish_order, purchase_steps, purchase_step2, purchase_step3

app_name = 'order'

urlpatterns = [
    path('finish/', finish_order, name='finish_order'),
    path('finish/<int:new_order_id>/', purchase_steps, name='purchase_steps'),
    path('finish/<int:new_order_id>/step2/', purchase_step2, name='purchase_step2'),
    path('finish/<int:new_order_id>/step3/', purchase_step3, name='purchase_step3'),
]