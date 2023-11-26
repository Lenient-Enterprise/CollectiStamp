from django.shortcuts import render, get_object_or_404, redirect

from .models import Product
from .models import Criteria
from .models import ProductReview
from .forms import ProductReviewForm

def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            return redirect('product_details', product_id=product_id)
    else:
        form = ProductReviewForm()

    return render(request, 'product/details.html', {'product': product, 'form': form})


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

    reviews = ProductReview.objects.filter(product=1)

    return render(request, 'product/product_catalog.html', {'products': products, 'criteria': criteria, reviews: reviews})
