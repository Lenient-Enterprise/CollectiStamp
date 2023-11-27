from django.shortcuts import render, redirect
from .forms import order_form_authenticated, order_form_not_authenticated

from .models import Order, OrderProduct, PaymentMethod
from datetime import date
from preorder import cart

from preorder.context_processor import total_cart
from preorder.views import delete_cart

from product.models import Product


def finish_order(request):
        
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
        
    return redirect(str(new_order_id)+"/")

def purchase_steps(request, new_order_id):
    order_products = OrderProduct.objects.filter(order_id=new_order_id)
    payment_methods = PaymentMethod.choices
    #products = [Product.objects.get(id=order_product.product_id) for order_product in order_products]

    return render(request, 'order/purchase_step1.html',
                  {'order_products': order_products,
                   'payment_methods': payment_methods,
                   #'products': products
                })
