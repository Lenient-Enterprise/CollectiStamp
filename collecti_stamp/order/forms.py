from django import forms
from .models import Order, PaymentMethod, DeliveryStatus, DeliveryMethod


class order_form_not_authenticated(forms.ModelForm):
    
    user_email=forms.CharField(label="user_email", required=True)

    delivery_address=forms.CharField(label="delivery_address", widget=forms.Textarea)
    
    #TODO: Falta añadir payment_method, delivery_status y delivery_method
    
class order_form_authenticated(forms.Form):
    
    delivery_address=forms.CharField(label="delivery_address", widget=forms.Textarea)
    
    #TODO: Falta añadir payment_method, delivery_status y delivery_method

class CustomerDataForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=False)
    delivery_address = forms.CharField(max_length=250, required=False)
    user_email = forms.EmailField(required=False)