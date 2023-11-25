from django.shortcuts import render, redirect
from preorder.cart import Cart
from product.models import Product

def view_cart(request):
    return(request, "cart.html")
    
def add_product(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.add_product(product=product)
    return redirect("Cart")

def decrement_product(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.decrement_product(product=product)
    return redirect("Cart")

def delete_product(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.delete_product(product=product)
    return redirect("Cart")

def delete_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.delete_cart()
    return redirect("Cart")