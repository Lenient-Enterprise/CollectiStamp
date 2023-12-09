# views.py
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from product.models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@require_http_methods(["GET"])
def home(request):
    # Obtén los tres productos más caros y los tres más baratos
    coins = Product.objects.all().filter(product_type="COIN").order_by('price')[:9]
    seals = Product.objects.all().filter(product_type="SEAL").order_by('price')[:9]

    # Combina ambas listas para mostrar en la plantilla
    products = coins | seals

    return render(request, 'base/home.html', {'products': products})
