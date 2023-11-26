from django.shortcuts import render


def finish_order(request, order_id):
    return render(request, 'orders/purchase_step1.html', {'order_id': order_id })
