from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from preorder.cart import Cart
from product.models import Product


class CartView(View):
    def get(self, request):
        return render(request, "preorder/cart.html")

class AddProductView(View):
    def get(self, request, product_id, amount):
        redirect_to = request.META.get('HTTP_REFERER', '/')
        cart = Cart(request)
        product = Product.objects.get(id=product_id)
        amount_final = amount
        if str(product_id) in cart.cart:
            amount_final += cart.cart[str(product_id)]["amount"]
        if amount_final > product.stock_amount:
            return redirect(f'{redirect_to}?message=No hay suficiente stock&status=Error')
        cart.add_product(product=product, amount=amount)
        if "status" in redirect_to:
            redirect_to = "/catalog/"
        return HttpResponseRedirect(redirect_to)

class DecrementProductCartView(View):
    def get(self, request, product_id, amount):
        cart = Cart(request)
        product = Product.objects.get(id=product_id)
        cart.decrement_product(product=product, amount=amount)
        return redirect("view_cart")
    
class DeleteProductCartView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = Product.objects.get(id=product_id)
        cart.delete_product(product=product)
        return redirect("view_cart")
    
class DeleteCartView(View):
    def get(self, request):
        cart = Cart(request)
        cart.delete_cart()
        return redirect("view_cart")