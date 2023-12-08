from django.urls import path
from .views import finish_order, PurchaseStep1View, PurchaseStep2View, PurchaseStep3View,create_payment,payment_success, payment_cancel
from . import views

app_name = 'order'

urlpatterns = [
    path('finish/', finish_order, name='finish_order'),
    path('finish/<int:new_order_id>/step1/', PurchaseStep1View.as_view(), name='purchase_step1'),
    path('finish/<int:new_order_id>/step2/', PurchaseStep2View.as_view(), name='purchase_step2'),
    path('finish/<int:new_order_id>/step3/', PurchaseStep3View.as_view(), name='purchase_step3'),
    path('create-payment/<int:order_id>/', create_payment, name='create_payment'),
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/cancel/', payment_cancel, name='payment_cancel'),
]