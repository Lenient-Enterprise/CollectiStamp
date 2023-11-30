from django.shortcuts import render, get_object_or_404

from .models import Product
from .models import Criteria


def product_details(request, product_id):  # Change the parameter name
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product/details.html', {'product': product})


from django.db.models import Q

def product_catalog(request):
    products = Product.objects.all()
    criteria = Criteria.objects.all()

    criteria1 = request.GET.get('criteria1')
    criteria2 = request.GET.get('criteria2')
    criteria3 = request.GET.get('criteria3')

    if criteria1:
        products = products.filter(criteria__id=criteria1)
    if criteria2:
        products = products.filter(criteria__id=criteria2)
    if criteria3:
        products = products.filter(criteria__id=criteria3)
     
    coins=products.filter(product_type="COIN")
    seals=products.filter(product_type="SEAL")
     
    return render(request, 'product/product_catalog.html', {'coins': coins, 'seals': seals, 'criteria': criteria})

