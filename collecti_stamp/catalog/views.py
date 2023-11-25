from django.shortcuts import render

from product.models import Product


# Create your views here.
def filter_product(request):
    products = Product.objects.all()

    # Filtros
    product_type = request.GET.get('product_type')
    name = request.GET.get('name')

    if product_type:
        print(product_type)
        products = products.filter(product_type=product_type)

    if name:
        products = products.filter(name=name)

    return render(request, 'product/product_catalog.html', {'products': products})
