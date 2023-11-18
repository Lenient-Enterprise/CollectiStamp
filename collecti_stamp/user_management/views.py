from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string, get_template
from django.urls import reverse
import re
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import CustomUserCreationForm,CustomUserEditionForm 
from .models import User
from collecti_stamp import settings


# Vista para iniciar sesión
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return render(request, 'collecti_stamp/home.html')
    else:
        form = AuthenticationForm()
    return render(request, 'customer/login.html', {'form': form})


# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return render(request, 'collecti_stamp/home.html')



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
                content = template.render({'verify_url': settings.BASE_URL + verify_url, 'username': user.username})
                message = EmailMultiAlternatives(
                    'Verificación de correo electrónico',
                    content,
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )

                message.attach_alternative(content, 'text/html')
                message.send()
                return render(request, 'collecti_stamp/home.html', {'message': 'Verificación de correo electrónico', 'status': 'Success'})
    else:
        form = CustomUserCreationForm()
    return render(request, 'customer/signin.html', {'form': form})

def validate_email(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(patron, email):
        return True
    else:
        return False



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

@login_required   
def edit_user_view(request, user_id):
    user=get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = CustomUserEditionForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            if validate_email(user.email):
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                verify_url = reverse('verify_email', args=[uid, token])
                template = get_template('customer/verification_email.html')
                content = template.render({'verify_url': settings.BASE_URL + verify_url, 'username': user.username})
                message = EmailMultiAlternatives(
                    'Verificación de correo electrónico',
                    content,
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )

                message.attach_alternative(content, 'text/html')
                message.send()
                return render(request, 'collecti_stamp/home.html', {'message': 'Verificación de correo electrónico', 'status': 'Success'})
    else:
        form = CustomUserEditionForm(instance=user)
    return render(request, 'customer/edit.html', {'form': form, 'user': user})


