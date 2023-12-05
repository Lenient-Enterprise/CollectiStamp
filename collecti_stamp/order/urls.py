from django.urls import path
from .views import finish_order, PurchaseStep1View, purchase_step2, PurchaseStep3View
from . import views

app_name = 'order'

urlpatterns = [
    path('finish/', finish_order, name='finish_order'),
    path('finish/<int:new_order_id>/step1/', PurchaseStep1View.as_view(), name='purchase_step1'),
    path('finish/<int:new_order_id>/step2/', purchase_step2, name='purchase_step2'),
    path('finish/<int:new_order_id>/step3/', PurchaseStep3View.as_view(), name='purchase_step3'),
]