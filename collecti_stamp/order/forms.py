from django import forms
from .models import Order, DeliveryMethod, PaymentMethod


class CustomerDataForm(forms.Form):
    user_name = forms.CharField(max_length=100, required=True)
    delivery_address = forms.CharField(max_length=250, required=True)
    user_email = forms.EmailField(required=True)
    
class delivery_method_selection(forms.Form):
    choices_with_default = [('', 'Seleccione metodo de entrega')] + list(DeliveryMethod.choices)
    delivery_method = forms.ChoiceField(choices=choices_with_default, required=True)

    def clean(self):
        cleaned_data = super().clean()
        delivery_method = cleaned_data.get("delivery_method")

        if not delivery_method or delivery_method == '':
            self.add_error('delivery_method', 'Por favor, seleccione un método de entrega.')
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