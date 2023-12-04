from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']

class EmailForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'usuario@dominio.com'}))

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '********'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '********'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Verificar que las contraseñas coincidan
        if password and confirm_password and password != confirm_password:
            self.add_error('password', 'Las contraseñas no coinciden.')
            self.add_error('confirm_password', 'Las contraseñas no coinciden.')

        # Verificar si la contraseña cumple con ciertos criterios (puedes personalizar esto)
        if password and len(password) < 8 and len(self.errors) == 0:
            self.add_error('password', 'La contraseña debe tener al menos 8 caracteres.')

        # Verificar si la contraseña es lo suficientemente fuerte según tus criterios
        if password and len(self.errors) == 0:
            if not any(char.isdigit() for char in password) and len(self.errors) == 0:
                self.add_error('password', 'La contraseña debe contener al menos un número.')

            elif not any(char.isupper() for char in password) and len(self.errors) == 0:
                self.add_error('password', 'La contraseña debe contener al menos una letra mayúscula.')

            elif not any(char.islower() for char in password) and len(self.errors) == 0:
                self.add_error('password', 'La contraseña debe contener al menos una letra minúscula.')

            elif not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/" for char in password) and len(self.errors) == 0:
                self.add_error('password', 'La contraseña debe contener al menos un carácter especial.')

        return cleaned_data
class CustomUserEditionForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'address', 'delivery_method', 'payment_method', 'first_name', 'last_name']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('El nombre de usuario ya está en uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('El correo electrónico ya está en uso.')
        return email


class CustomAuthenticationForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'usuario@dominio.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '********'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            if not User.objects.filter(email=email).exists():
                self.add_error('email', 'El correo electrónico no está registrado.')
            else:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    self.add_error('password', 'La contraseña es incorrecta.')
                elif not user.email_verified:
                    self.add_error('email', 'El correo electrónico no está verificado.')
        return cleaned_data

    def get_user(self):
        email = self.cleaned_data['email']
        return User.objects.get(email=email)

