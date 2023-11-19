# company/urls.py
from django.urls import path
from .views import company_details

urlpatterns = [
    path('about-us/', company_details, name='company_details'),
]
