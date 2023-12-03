from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404

from .forms import CustomerDataForm, delivery_method_selection, PaymentMethodForm
from .models import Order, OrderProduct, PaymentMethod, DeliveryMethod, DeliveryStatus
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

    return redirect(str(new_order_id)+"/step1/")

@require_http_methods(["GET", "POST"])
def purchase_step1(request, new_order_id):
    order_products = OrderProduct.objects.filter(order_id=new_order_id)
    payment_methods = PaymentMethod.choices

    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            order = get_object_or_404(Order, id=new_order_id)
            order.payment_method = form.cleaned_data['payment_method']
            order.save()
            return redirect('order:purchase_step2', new_order_id=new_order_id)
        else:
            products = get_order_products(order_products, new_order_id)
            return render(request, 'order/purchase_step1.html',
                          {'order_products': order_products, 'payment_methods': payment_methods,
                           'order_id': new_order_id, 'form': form, 'products': products})
    else:
        form = PaymentMethodForm()
        products = get_order_products(order_products, new_order_id)
        return render(request, 'order/purchase_step1.html', {'order_products': order_products, 'payment_methods': payment_methods, 'order_id': new_order_id, 'form': form, 'products': products})

@require_http_methods(["GET", "POST"])
def purchase_step2(request, new_order_id):
    order_products = OrderProduct.objects.filter(order_id=new_order_id)
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
            products = get_order_products(order_products, new_order_id)
            return render(request, 'order/purchase_step2.html',
                          {'order_products': order_products, 'new_order_id': new_order_id,
                           'delivery_method': delivery_choices, 'form': form, 'products': products})
    else:
        form = delivery_method_selection()
        products = get_order_products(order_products, new_order_id)
        return render(request, 'order/purchase_step2.html', {'order_products': order_products, 'new_order_id': new_order_id, 'delivery_method': delivery_choices, 'form': form, 'products': products})

@require_http_methods(["POST", "GET"])
def purchase_step3(request, new_order_id):
    order_products = OrderProduct.objects.filter(order_id=new_order_id)
    payment_methods = PaymentMethod.choices

    if request.method == 'POST':
        customer_form = CustomerDataForm(request.POST)
        if customer_form.is_valid():
            request.session['customer_data'] = customer_form.cleaned_data
            purchase_failed = False

            for order_product in order_products:
                product = get_object_or_404(Product, id=order_product.product_id.first().id)
                if product.stock_amount < order_product.quantity:
                    purchase_failed = True
                    break

            if purchase_failed == False:
                order = get_object_or_404(Order, id=new_order_id)
                order.user_email = customer_form.cleaned_data['user_email']
                order.user_name = customer_form.cleaned_data['nombre']
                order.delivery_address = customer_form.cleaned_data['delivery_address']
                order.delivery_status = DeliveryStatus.STATUS_A
                order.order_is_finished = True
                for order_product in order_products:
                    product = get_object_or_404(Product, id=order_product.product_id.first().id)
                    product.stock_amount -= order_product.quantity
                    product.save()
                order.save()
                return redirect('/?message=Compra Realizada&status=Success')
            else:
                return redirect('/?message=Uno de los productos se ha agotado&status=Error')
        else:
            form = CustomerDataForm()
            products = get_order_products(order_products, new_order_id)
            return render(request, 'order/purchase_step3.html',
                          {'order_products': order_products, 'payment_methods': payment_methods,
                           'new_order_id': new_order_id, 'customer_form': form, 'products': products})
    else:
        form = CustomerDataForm()
        products = get_order_products(order_products, new_order_id)
        return render(request, 'order/purchase_step3.html', {'order_products': order_products, 'payment_methods': payment_methods, 'new_order_id': new_order_id, 'customer_form': form, 'products': products})


def get_order_products(order_products, order_id):
    products = []
    for order_product in order_products:
        product = get_object_or_404(Product, id=order_product.product_id.first().id)
        products.append(product)
    return products
