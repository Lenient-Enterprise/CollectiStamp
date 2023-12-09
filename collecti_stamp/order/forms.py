from django import forms

from .models import DeliveryMethod, PaymentMethod


class CustomerDataForm(forms.Form):
    user_name = forms.CharField(max_length=100, required=True)
    delivery_address = forms.CharField(max_length=250, required=True)
    user_email = forms.EmailField(required=True)
    

class DeliveryMethodSelection(forms.Form):
    default_choice = 'default'
    delivery_method = forms.ChoiceField(
        choices=[(default_choice, 'Selecciona un método de entrega')] + list(DeliveryMethod.choices),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es requerido.'}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delivery_method'].label = 'Método de Entrega'

    def clean_delivery_method(self):
        delivery_method = self.cleaned_data['delivery_method']
        if delivery_method == self.default_choice:
            raise forms.ValidationError("Por favor, selecciona un método de entrega válido.")
        return delivery_method


class PaymentMethodForm(forms.Form):
    default_choice = 'default'
    payment_method = forms.ChoiceField(
        choices=[(default_choice, 'Selecciona un método de pago')] + list(PaymentMethod.choices),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'Este campo es requerido.'}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Establecer etiqueta y texto de ayuda en español
        self.fields['payment_method'].label = 'Método de Pago'
        self.fields['payment_method'].help_text = 'Selecciona un método de pago'

    def clean_payment_method(self):
        payment_method = self.cleaned_data['payment_method']
        if payment_method == self.default_choice:
            raise forms.ValidationError("Por favor, selecciona un método de pago válido.")
        return payment_method

    def add_error(self, field, error):
        if field == '__all__':
            error = "Por favor, completa el formulario correctamente."
        super().add_error(field, error)
