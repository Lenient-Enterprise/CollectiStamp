from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .forms import CustomerDataForm, delivery_method_selection
from .models import Order, OrderProduct, PaymentMethod, DeliveryMethod
from datetime import date
from preorder import cart

from preorder.context_processor import total_cart
from preorder.views import delete_cart

from product.models import Product
from customer.models import User


@require_http_methods(["POST"])
def finish_order(request):
    new_order = Order.objects.create(
        user_email="",
        order_date=date.today(),
        order_total=total_cart(request).get("total_cart", 0),
        order_is_finished=False,
        payment_method='',
        delivery_status='',
        delivery_method='',
        delivery_cost=3.99,
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

    return redirect(str(new_order_id) + "/")

@require_http_methods(["GET", "POST"])
def purchase_steps(request, new_order_id):
    order_products = OrderProduct.objects.filter(order_id=new_order_id)
    payment_methods = PaymentMethod.choices

    if request.method == 'POST':
        # Lógica para manejar el formulario en caso de solicitud POST
        customer_form = CustomerDataForm(request.POST)
        if customer_form.is_valid():
            request.session['customer_data'] = customer_form.cleaned_data
            return redirect('order:purchase_complete', new_order_id=new_order_id)
    else:
        # Lógica para manejar la solicitud GET
        customer_form = CustomerDataForm()

    return render(request, 'order/purchase_step1.html', {'order_products': order_products, 'payment_methods': payment_methods, 'order_id': new_order_id, 'customer_form': customer_form})

@require_http_methods(["POST"])
def purchase_step2(request, new_order_id):
    delivery_choices = DeliveryMethod.choices
    if request.method == 'POST':
        form = delivery_method_selection(request.POST)
        if form.is_valid():
            order = Order.objects.get(id=new_order_id)
            delivery_method = form.cleaned_data['delivery_method']
            delivery_address = form.cleaned_data['delivery_address']
            if delivery_method == 'PICK':
                delivery_address = 'Recogida en tienda'
            order.delivery_method = delivery_method
            order.delivery_address = delivery_address
            order.save()
            return redirect('order:purchase_step3', new_order_id=new_order_id)
    else:
        form = delivery_method_selection()
    return render(request, 'order/purchase_step2.html', {'new_order_id': new_order_id, 'delivery_method': delivery_choices, 'form': form})

@require_http_methods(["POST"])
def purchase_step3(request, new_order_id):
    order_products = OrderProduct.objects.filter(order_id=new_order_id)
    payment_methods = PaymentMethod.choices

    if request.method == 'POST':
        customer_form = CustomerDataForm(request.POST)
        if customer_form.is_valid():
            request.session['customer_data'] = customer_form.cleaned_data
            return redirect('order:purchase_complete', new_order_id=new_order_id)

    if request.user.is_authenticated:
        user_data, created = User.objects.get_or_create(id=request.user.id)
        customer_form = CustomerDataForm(instance=user_data)
    else:
        customer_form = CustomerDataForm()

    delete_cart(request)
    return render(request, 'order/purchase_step3.html', {'order_products': order_products, 'payment_methods': payment_methods, 'customer_form': customer_form, 'new_order_id': new_order_id})