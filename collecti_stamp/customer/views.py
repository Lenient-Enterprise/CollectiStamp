from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from collecti_stamp import settings
from .forms import CustomUserCreationForm, EmailForm, PasswordForm, CustomUserEditionForm, CustomAuthenticationForm
from order.models import DeliveryMethod, PaymentMethod
from .models import User
from .utils import validate_email, get_user
from collecti_stamp import settings

# Vista para iniciar sesión
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views import View
from .forms import CustomAuthenticationForm
from .order.models import Order


class LoginView(View):
    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, 'customer/login.html', {'form': form})

    def post(self, request):
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/')
        else:
            return render(request, 'customer/login.html', {'form': form})


# Vista para cerrar sesión
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


# Vista para registro de usuario
class SigninView(View):
    def get(self, request):

        form = CustomUserCreationForm()
        return render(request, 'customer/signin.html',
                      {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid() and User.objects.filter(email=form.cleaned_data['email']).count() == 0:
            user = form.save()

            if validate_email(user.email):
                # Asignar nombre de usuario
                user.username = user.email.split('@')[0]
                user.save()

                # Generar el token único
                token = default_token_generator.make_token(user)

                # Generar la URL de verificación por correo electrónico
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                verify_url = reverse('verify_email', args=[uid, token])

                # Enviar el correo electrónico de verificación
                template = get_template('customer/verification_email.html')
                content = template.render(
                    {'verify_url': request.build_absolute_uri('/') + verify_url, 'username': user.username})
                message = EmailMultiAlternatives(
                    'Verificación de correo electrónico',
                    content,
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )

                message.attach_alternative(content, 'text/html')
                message.send()
                return redirect('/?message=Verificación de correo electrónico&status=Success')
        return render(request, 'customer/signin.html',
                      {'form': form})


class VerifyEmailView(View):

    def get(self, request, uidb64, token):
        user = get_user(uidb64)
        if user is not None and default_token_generator.check_token(user, token):
            user.email_verified = True
            user.save()
            return redirect('/?message=Correo electrónico verificado&status=Success')
        else:
            return redirect('/?message=Correo electrónico no verificado&status=Error')


class RequestPasswordResetView(View):
    def get(self, request):
        form = EmailForm()
        return render(request, 'customer/make_petition_form.html', {'form': form})

    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, email=form.cleaned_data['email'])

            if validate_email(user.email):
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                new_password_url = reverse('change_password', args=[uid, token])

                template = get_template('customer/password_email.html')
                content = template.render(
                    {'new_password_url': request.build_absolute_uri('/') + new_password_url, 'username': user.username})
                message = EmailMultiAlternatives(
                    'Cambio de contraseña',
                    content,
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )

                message.attach_alternative(content, 'text/html')
                message.send()
                return redirect('/?message=Petición de cambio de contraseña enviada&status=Info')

        return render(request, 'customer/request_password_reset.html', {'form': form})

class ChangePasswordView(View):

    def get(self, request, uidb64, token):
        user = get_user(uidb64)
        if user is not None and default_token_generator.check_token(user, token):
            form = PasswordForm()
            return render(request, 'customer/change_password_form.html', {'form': form})
        else:
            return redirect('/?message=Error al cambiar la contraseña&status=Error')

    def post(self, request, uidb64, token):
        user = get_user(uidb64)
        if user is not None and default_token_generator.check_token(user, token):
            form = PasswordForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['password'])
                user.save()
                return redirect('/?message=Contraseña cambiada&status=Success')
        return redirect('/?message=Error al cambiar la contraseña&status=Error')


class EditUserView(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = CustomUserEditionForm(instance=user)
        return render(request, 'customer/edit.html', {'form': form, 'user': user})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = CustomUserEditionForm(request.POST, instance=user)
        if form.is_valid():
            if form.cleaned_data['email'] != user.email:
                orders = Order.objects.filter(user_email=form.cleaned_data['email'])
                for order in orders:
                    order.user_email = form.cleaned_data['email']
                    order.save()
            form.save()
            return redirect('/?message=Usuario editado&status=Success')
        else:
            return render(request, 'customer/edit.html', {'form': form, 'user': user})

def get_user(self, uidb64):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        return user
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None
