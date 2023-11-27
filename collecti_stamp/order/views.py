from django.shortcuts import render, redirect
from .forms import order_form_authenticated, order_form_not_authenticated
from .forms import CustomerDataForm
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
    return render(request, 'order/purchase_step1.html', {'order_products': order_products, 'payment_methods': payment_methods})

def purchase_step2(request, new_order_id):
    # Lógica para el paso 2
    # ...

    return render(request, 'order/purchase_step2.html', {'new_order_id': new_order_id})

def purchase_step3(request, new_order_id):
    order_products = OrderProduct.objects.filter(order_id=new_order_id)
    payment_methods = PaymentMethod.choices

    if request.method == 'POST':
        customer_form = CustomerDataForm(request.POST)
        if customer_form.is_valid():
            # Guardar los datos del cliente en la sesión
            request.session['customer_data'] = customer_form.cleaned_data
            return redirect('order:purchase_complete', new_order_id=new_order_id)

    customer_form = CustomerDataForm()
    return render(request, 'order/purchase_step3.html', {'order_products': order_products, 'payment_methods': payment_methods, 'customer_form': customer_form, 'new_order_id': new_order_id})
