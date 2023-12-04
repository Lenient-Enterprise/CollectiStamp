from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from order.models import Order

# Create your views here.
def get_order_tracking(request, code):  # Change the parameter name
    order = get_object_or_404(Order, code=code)
    return render(request, 'postorder/order_details.html', {'order': order})

@login_required
def list_order_tracking(request):
    orders = Order.objects.filter(user_email=request.user.email)
    return render(request, 'postorder/list.html', {'orders': orders})