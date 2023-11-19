
from django.shortcuts import render, get_object_or_404

from .models import Product
from .models import Criteria


def product_details(request, product_id):  # Change the parameter name
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product/details.html', {'product': product})

def product_catalog(request):
    products = Product.objects.all()
    criteria = Criteria.objects.all()
    return render(request, 'product/product_catalog.html', {'products': products, 'criteria': criteria})