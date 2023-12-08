from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404

from preorder.cart import Cart

from .forms import CustomerDataForm, DeliveryMethodSelection, PaymentMethodForm
from .models import Order, OrderProduct, PaymentMethod, DeliveryMethod, DeliveryStatus
from datetime import date

from preorder.context_processor import total_cart

from product.models import Product


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
        delivery_cost=0,
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

class PurchaseStep1View(View):
    template_name = 'order/purchase_step1.html'

    def get(self, request, new_order_id):
        order_products = OrderProduct.objects.filter(order_id=new_order_id)
        payment_methods = PaymentMethod.choices
        user_is_logged_in = request.user.is_authenticated
        form = PaymentMethodForm(request.POST)
        products = get_order_products(order_products)
        return render(request, self.template_name,
               {
                'order_products': order_products,
                'payment_methods': payment_methods,
                'order_id': new_order_id,
                'form': form, 'products': products,
                'user_is_logged_in': user_is_logged_in
                })

    def post(self, request, new_order_id):

        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            order = get_object_or_404(Order, id=new_order_id)
            order.payment_method = form.cleaned_data['payment_method']
            order.save()
            return redirect('order:purchase_step2', new_order_id=new_order_id)

        order_products = OrderProduct.objects.filter(order_id=new_order_id)
        payment_methods = PaymentMethod.choices
        user_is_logged_in = request.user.is_authenticated
        form = PaymentMethodForm(request.POST)
        products = get_order_products(order_products)
        return render(request, self.template_name,
               {
                'order_products': order_products,
                'payment_methods': payment_methods,
                'order_id': new_order_id,
                'form': form, 'products': products,
                'user_is_logged_in': user_is_logged_in
                })
        
        
class PurchaseStep2View(View):
    template_name = 'order/purchase_step2.html'
    
    def get(self, request, new_order_id):
        order_products = OrderProduct.objects.filter(order_id=new_order_id)
        delivery_method = DeliveryMethod.choices
        user_is_logged_in = request.user.is_authenticated
        form = DeliveryMethodSelection(request.POST)
        products = get_order_products(order_products)
        return render(request, self.template_name,
               {
                'order_products': order_products,
                'delivery_method': delivery_method,
                'order_id': new_order_id,
                'form': form,
                'products': products,
                'user_is_logged_in': user_is_logged_in
                })
        
    def post(self, request, new_order_id):
        form = DeliveryMethodSelection(request.POST)
        if form.is_valid():
            order = get_object_or_404(Order, id=new_order_id)
            order.delivery_method = form.cleaned_data['delivery_method']
            
            delivery_cost = 0.0
            if order.delivery_method == DeliveryMethod.STANDARD_SHIPPING and order.order_total < 50:
                delivery_cost = 3.0
            elif order.delivery_method == DeliveryMethod.EXPRESS_SHIPPING and order.order_total < 50:
                delivery_cost = 5.0
            order.delivery_cost = delivery_cost
            
            order.save()
            return redirect('order:purchase_step3', new_order_id=new_order_id)
        order_products = OrderProduct.objects.filter(order_id=new_order_id)
        delivery_method = DeliveryMethod.choices
        user_is_logged_in = request.user.is_authenticated
        form = DeliveryMethodSelection(request.POST)
        products = get_order_products(order_products)
        return render(request, self.template_name,
               {
                'order_products': order_products,
                'delivery_method': delivery_method,
                'order_id': new_order_id,
                'form': form, 'products': products,
                'user_is_logged_in': user_is_logged_in
                })


class PurchaseStep3View(View):
    template_name = 'order/purchase_step3.html'

    def get(self, request, new_order_id):
        order_products = OrderProduct.objects.filter(order_id=new_order_id)
        payment_methods = PaymentMethod.choices
        user_is_logged_in = request.user.is_authenticated
        
        order = get_object_or_404(Order, id=new_order_id)
        delivery_cost = order.delivery_cost

        form = CustomerDataForm()
        products = get_order_products(order_products)

        return render(request, self.template_name, {
            'order_products': order_products,
            'payment_methods': payment_methods,
            'new_order_id': new_order_id,
            'delivery_cost': delivery_cost,
            'customer_form': form,
            'products': products,
            'user_is_logged_in': user_is_logged_in,
        })

    def post(self, request, new_order_id):
        customer_form = CustomerDataForm(request.POST)

        if customer_form.is_valid():
            order = get_object_or_404(Order, id=new_order_id)
            order.user_email = customer_form.cleaned_data['user_email']
            order.user_name = customer_form.cleaned_data['user_name']
            order.delivery_address = customer_form.cleaned_data['delivery_address']
            order.delivery_status = DeliveryStatus.IN_WAREHOUSE
            order.order_is_finished = True

            order_products = OrderProduct.objects.filter(order_id=new_order_id)

            for order_product in order_products:
                product = get_object_or_404(Product, id=order_product.product_id.first().id)
                if product.stock_amount < order_product.quantity:
                    return redirect('/?message=Uno de los productos se ha agotado&status=Error')

                product.stock_amount -= order_product.quantity
                product.save()

            order.save()
            
            cart = Cart(request)
            cart.delete_cart()
            
            return redirect('/?message=Compra Realizada&status=Success')

        order_products = OrderProduct.objects.filter(order_id=new_order_id)
        payment_methods = PaymentMethod.choices
        user_is_logged_in = request.user.is_authenticated

        form = customer_form
        products = get_order_products(order_products)

        return render(request, self.template_name, {
            'order_products': order_products,
            'payment_methods': payment_methods,
            'new_order_id': new_order_id,
            'customer_form': form,
            'products': products,
            'user_is_logged_in': user_is_logged_in,
        })



def get_order_products(order_products):
    products = []
    for order_product in order_products:
        product = get_object_or_404(Product, id=order_product.product_id.first().id)
        products.append(product)
    return products
