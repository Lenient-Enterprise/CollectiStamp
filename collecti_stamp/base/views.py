# views.py
from django.shortcuts import render
from product.models import Product

def home(request):
    # Obtén los tres productos más caros y los tres más baratos
    expensive_products = Product.objects.all().order_by('-price')[:3]
    cheap_products = Product.objects.all().order_by('price')[:3]

    # Combina ambas listas para mostrar en la plantilla
    products = expensive_products | cheap_products

    return render(request, 'base/home.html', {'products': products})
