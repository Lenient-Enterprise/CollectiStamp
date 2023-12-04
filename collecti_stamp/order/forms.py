from django import forms
from .models import Order, DeliveryMethod, PaymentMethod


class CustomerDataForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=False)
    delivery_address = forms.CharField(max_length=250, required=False)
    user_email = forms.EmailField(required=False)
    
class delivery_method_selection(forms.Form):
    delivery_method = forms.ChoiceField(choices=DeliveryMethod.choices)
    delivery_address = forms.CharField(required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        delivery_method = cleaned_data.get("delivery_method")
        delivery_address = cleaned_data.get("delivery_address")

        if delivery_method != 'PICK' and not delivery_address:
            self.add_error('delivery_address', 'Este campo es obligatorio si el método de entrega no es "Recogida en tienda"')
        return cleaned_data

class PaymentMethodForm(forms.Form):
    default_choice = 'default'
    payment_method = forms.ChoiceField(
        choices=[(default_choice, 'Selecciona un método de pago')] + list(PaymentMethod.choices),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean_payment_method(self):
        payment_method = self.cleaned_data['payment_method']
        if payment_method == self.default_choice:
            raise forms.ValidationError("Por favor, seleccione un método de pago válido.")
        return payment_method