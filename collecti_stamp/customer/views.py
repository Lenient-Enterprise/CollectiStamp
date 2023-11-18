from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from collecti_stamp import settings
from .forms import CustomUserCreationForm, EmailForm, PasswordForm
from .models import User
from .utils import validate_email, get_user


# Vista para iniciar sesión
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print(form.errors)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/base')
    else:
        form = AuthenticationForm()
    return render(request, 'customer/login.html', {'form': form})


# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('/base')


# Vista para registro de usuario
def signin_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid() and User.objects.filter(email=form.cleaned_data['email']).count() == 0 and User.objects.filter(
                username=form.cleaned_data['username']).count() == 0:
            user = form.save()

            if validate_email(user.email):
                # Generar el token único
                token = default_token_generator.make_token(user)

                # Generar la URL de verificación por correo electrónico
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                verify_url = reverse('verify_email', args=[uid, token])

                # Enviar el correo electrónico de verificación
                template = get_template('customer/verification_email.html')
                content = template.render({'verify_url': settings.BASEURL + verify_url, 'username': user.username})
                message = EmailMultiAlternatives(
                    'Verificación de correo electrónico',
                    content,
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )

                message.attach_alternative(content, 'text/html')
                message.send()
                return redirect('/base?message=Verificación de correo electrónico&status=Success')
    else:
        form = CustomUserCreationForm()
    return render(request, 'customer/signin.html', {'form': form})


def verify_email(request, uidb64, token):
    user = get_user(uidb64)
    if user is not None and default_token_generator.check_token(user, token):
        user.email_verified = True
        user.save()
        return redirect('/base?message=Correo electrónico verificado&status=Success')
    else:
        return redirect('/base?message=Correo electrónico no verificado&status=Error')

def request_password_reset(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, email=form.cleaned_data['email'])

            if validate_email(user.email):
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                new_password_url = reverse('change_password', args=[uid, token])

                template = get_template('customer/password_email.html')
                content = template.render(
                    {'new_password_url': settings.BASE_URL + new_password_url, 'username': user.username})
                message = EmailMultiAlternatives(
                    'Cambio de contraseña',
                    content,
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )

                message.attach_alternative(content, 'text/html')
                message.send()
                return redirect('/base?message=Petición de cambio de contraseña enviada&status=Info')

        return render(request, 'customer/request_password_reset.html', {'form': form})
    else:
        form = EmailForm()
        return render(request, 'customer/make_petition_form.html', {'form': form})

def change_password(request, uidb64, token):
    user = get_user(uidb64)
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = PasswordForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['password'])
                user.save()
                return redirect('/base?message=Contraseña cambiada&status=Success')
        else:
            form = PasswordForm()
            return render(request, 'customer/change_password_form.html', {'form': form})
    else:
        return redirect('/base?message=Error al cambiar la contraseña&status=Error')