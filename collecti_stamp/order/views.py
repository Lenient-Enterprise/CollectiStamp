from django.shortcuts import render, redirect
from .forms import order_form_authenticated, order_form_not_authenticated

from .models import Order, OrderProduct
from datetime import date
from preorder import cart

from preorder.context_processor import total_cart
from preorder.views import delete_cart


def finish_order(request):
    if request.method == 'POST':
        if 'cart' in request.session:
            if not request.user.is_authenticated:
                form = order_form_not_authenticated(request.POST)
                if form.is_valid():
                    user_email = form.cleaned_data['user_email']
            else:
                form = order_form_authenticated(request.POST)
                if form.is_valid():
                    user_email = request.user.email
        delivery_address = form.cleaned_data.get('delivery_address', '')
        payment_method = form.cleaned_data.get('payment_method','')
        delivery_status = form.cleaned_data.get('delivery_status','')
        delivery_method = form.cleaned_data.get('delivery_method','')
        
        new_order = Order.objects.create(
            user_email="",
            order_date=date.today(),
            order_total=0,       # Cambiar
            order_is_finished=False,
            payment_method='',
            delivery_status='',
            delivery_method='',
            delivery_cost=3.99,  # Cambiar, valor por defecto de 3.99
            delivery_address='',
        )
        new_order.save()
        new_order_id = new_order.id
        cart = request.session['cart']
        for product_id, product_info in cart.items():
            order_product = OrderProduct.objects.create(
                quantity=product_info['amount']
            )
            order_product.order_id.set([new_order])
            order_product.product_id.set([product_id])
            order_product.save()

        delete_cart(request)
        
        return redirect('finish_order', new_order_id=new_order.id)

    else:
        if not request.user.is_authenticated:
            return redirect('order_form_not_authenticated')
        else:
            return redirect('order_form_authenticated')
