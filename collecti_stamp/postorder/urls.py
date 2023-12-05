
from django.urls import path

from postorder.views import get_order_tracking


urlpatterns = [
    path('<uuid:code>', get_order_tracking, name='order_details'),
]