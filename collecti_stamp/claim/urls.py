
from django.urls import path

from .views import CreateClaimView

urlpatterns = [
    path('create/<int:product_id>/', CreateClaimView.as_view(), name='create_claim'),
]