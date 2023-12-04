from django.shortcuts import get_object_or_404, render

from order.models import Order

# Create your views here.
def get_order_tracking(request, code):  # Change the parameter name
    order = get_object_or_404(Order, code=code)
    return render(request, 'postorder/details.html', {'order': order})