
from django.shortcuts import render, get_object_or_404

from .models import Product


def product_details(request, product_id):  # Change the parameter name
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product/details.html', {'product': product})