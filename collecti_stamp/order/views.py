from django.shortcuts import render, redirect
from collecti_stamp.order.forms import order_form_authenticated, order_form_not_authenticated

from collecti_stamp.order.models import Order, OrderProduct
from datetime import date
from collecti_stamp.preorder import cart

from collecti_stamp.preorder.context_processor import total_cart
from collecti_stamp.preorder.views import delete_cart


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
        delivery_address = form.cleaned_data['delivery_address']
        payment_method = form.cleaned_data['payment_method']
        delivery_status = form.cleaned_data['delivery_status']
        delivery_method = form.cleaned_data['delivery_method']
        
        new_order = Order.objects.create(
            user_email=user_email,
            order_date=date.today(),
            order_total=total_cart,
            order_is_finished=False,
            payment_method=payment_method,
            delivery_status=delivery_status,
            delivery_method=delivery_method,
            delivery_cost=3.99,  # Cambiar, valor por defecto de 3.99
            delivery_address=delivery_address,
        )
        new_order.save()
        new_order_id = new_order.id
        cart = request.session['cart']
        for product_id, name, price, amount, image, stock_amount in cart.items():
            order_product = OrderProduct.objects.create(
                order_id = new_order_id,
                product_id = product_id,
                quantity = amount,
                )
            order_product.save()
        delete_cart()
        
        return redirect('purchase_confirmation', {"new_order": new_order})

    else:
        if not request.user.is_authenticated:
            return redirect('order_form_not_authenticated')
        else:
            return redirect('order_form_authenticated')
