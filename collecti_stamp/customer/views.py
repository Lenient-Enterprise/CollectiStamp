from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from collecti_stamp import settings
from .forms import CustomUserCreationForm
from .models import User
from .utils import validate_email


# Vista para iniciar sesión
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
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
        if form.is_valid():
            user = form.save(commit=False)

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
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.verify_email = True
        user.save()
        return render(request, 'customer/verification_success.html')
    else:
        return render(request, 'customer/verification_error.html')
