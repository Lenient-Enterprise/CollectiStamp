# forms.py
from django import forms
from .models import ProductReview

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['username', 'name', 'description']
        labels = {
            'username': 'Autor de la reseña',
            'name': 'Título de la reseña',
            'description': 'Descripción',
        }