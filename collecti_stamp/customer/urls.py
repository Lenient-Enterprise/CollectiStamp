from django.urls import path

from .views import LoginView, LogoutView, SigninView, VerifyEmailView, RequestPasswordResetView, ChangePasswordView, \
    EditUserView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('verify_email/<str:uidb64>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('password-reset/', RequestPasswordResetView.as_view(), name='request_password_reset'),
    path('change-password/<str:uidb64>/<str:token>/', ChangePasswordView.as_view(), name='change_password'),
    path('edit/<int:user_id>', EditUserView.as_view(), name='edit')
]