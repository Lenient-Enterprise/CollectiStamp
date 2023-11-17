from django.urls import path

from . import views
from .views import login_view, logout_view, signin_view,edit_user_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signin/', signin_view, name='signin'),
    path('verify_email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    path('edit/<int:user_id>', edit_user_view, name='edit'),

]