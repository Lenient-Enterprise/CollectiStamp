import re

from base.views import home
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from order.models import Order


# Create your views here.
def get_order_tracking(request, code):  # Change the parameter name
    order = get_object_or_404(Order, code=code)
    state_name = {
        'IN_WAREHOUSE': 'En almacén',
        'ON_THE_WAY': 'En camino',
        'DELIVERED': 'Entregado',
    }
    delivery_methods = {
        'STANDARD_SHIPPING': 'Envío estándar',
        'EXPRESS_SHIPPING': 'Envío express',
        'PICKUP_IN_STORE': 'Recogida en tienda',
    }
    payment_methods = {
        'CASH_ON_DELIVERY': 'Contrarrembolso',
        'PAYPAL': 'PayPal',
    } 
    state=state_name.get(order.delivery_status)
    delivery_method=delivery_methods.get(order.delivery_method)
    payment_method=payment_methods.get(order.payment_method)
    return render(request, 'postorder/order_details.html', {'order': order, 'state':state,'delivery_method':delivery_method,'payment_method':payment_method})

@require_http_methods(["GET"])
def get_order_tracking_finder(request):  # Change the parameter name
    code = request.GET.get('code')
    guiones= re.sub(r'[^-]', '', code)
    if (len(code) == 36) and (len(guiones)==4) and (Order.objects.filter(code=code).count()>0):
        order= Order.objects.filter(code=code).first()
        state_name = {
            'IN_WAREHOUSE': 'En almacén',
            'ON_THE_WAY': 'En camino',
            'DELIVERED': 'Entregado',
        }
        delivery_methods = {
            'STANDARD_SHIPPING': 'Envío estándar',
            'EXPRESS_SHIPPING': 'Envío express',
            'PICKUP_IN_STORE': 'Recogida en tienda',
        }
        payment_methods = {
            'CASH_ON_DELIVERY': 'Contrarrembolso',
            'PAYPAL': 'PayPal',
        } 
        state=state_name.get(order.delivery_status)
        delivery_method=delivery_methods.get(order.delivery_method)
        payment_method=payment_methods.get(order.payment_method)
        return render(request, 'postorder/order_details.html', {'order': order, 'state':state,'delivery_method':delivery_method,'payment_method':payment_method})
    else:
        return home(request)
    
@login_required
def list_order_tracking(request):
    orders = Order.objects.filter(user_email=request.user.email)
    return render(request, 'postorder/order_list.html', {'orders': orders})
