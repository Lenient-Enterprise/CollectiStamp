from django.shortcuts import render, get_object_or_404

from .models import Product
from .models import Criteria
from .models import Category


def product_details(request, product_id):  # Change the parameter name
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product/details.html', {'product': product})


from django.db.models import Q

def product_catalog(request):
    products = Product.objects.all()
    criteria = Criteria.objects.all()
    categories= list(Product.objects.values('category').distinct().values_list('category', flat=True))
    category_names = {
        'ANCIENT': 'Antiguo',
        'COMIC_BOOK': 'Comic',
        'VIDEOGAME': 'Videojuego',
        'HISTORICAL': 'Histórico',
        'NOVELTY': 'Novedad',
    }   
    category_tuples = [(category, category_names.get(category, 'Desconocido')) for category in categories]
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
     
    return render(request, 'product/product_catalog.html', {'coins': coins, 'seals': seals, 'criteria': criteria, 'categories':category_tuples})

