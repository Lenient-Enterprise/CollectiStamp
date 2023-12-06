from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

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
        'PAYMENT_GATEWAY': 'Pasarelas de Pago',
    } 
    state=state_name.get(order.delivery_status)
    delivery_method=delivery_methods.get(order.delivery_method)
    payment_method=payment_methods.get(order.payment_method)
    return render(request, 'postorder/order_details.html', {'order': order, 'state':state,'delivery_method':delivery_method,'payment_method':payment_method})


@login_required
def list_order_tracking(request):
    orders = Order.objects.filter(user_email=request.user.email)
    return render(request, 'postorder/order_list.html', {'orders': orders})