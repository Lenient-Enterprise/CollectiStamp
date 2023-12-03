from django.shortcuts import render

from product.models import Criteria, Product

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
    product_type = request.GET.get('product_type')
    name = request.GET.get('name')

    if criteria1:
        products = products.filter(criteria__id=criteria1)
    if criteria2:
        products = products.filter(criteria__id=criteria2)
    if criteria3:
        products = products.filter(criteria__id=criteria3)
    if product_type:
        products = products.filter(product_type=product_type)
    if name:
        products = products.filter(name=name)
     
    return render(request, 'product/product_catalog.html', {'products': products, 'criteria': criteria, 'categories':category_tuples})
