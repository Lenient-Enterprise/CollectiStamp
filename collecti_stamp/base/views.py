# views.py
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from product.models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@require_http_methods(["GET"])
def home(request):
    # Obtén los tres productos más caros y los tres más baratos
    coins = Product.objects.all().filter(product_type="COIN").order_by('price')
    seals = Product.objects.all().filter(product_type="SEAL").order_by('price')

    # Combina ambas listas para mostrar en la plantilla
    products = coins | seals

    # Cambio a 10 productos por página
    paginator = Paginator(products, 20)  # Mostrar 20 productos por página
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, mostrar la primera página
        products = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango (página que no existe), mostrar la última página
        products = paginator.page(paginator.num_pages)

    return render(request, 'base/home.html', {'products': products})
