class Cart:
    def __init__(self, request):
        self.request = request
        self.sesion = request.session
        cart = self.sesion.get("cart")
        if not cart:
            self.session["cart"] = {}
            self.cart = self.sesion["cart"]
        else:
            self.cart = cart
            
    def seve_cart(self):
        self.session["cart"] = self.cart
        self.sesion.modified = True
            
    def add_product(self, product):
        product_id = str(product.id)
        if product_id not in self.cart.keys():
            self.cart[product_id] = {
                "product_id": product_id,
                "name": product.name,
                "price": product.price,
                "amount": 1,
            }
        else:
            self.cart[product_id]["amount"] += 1
        self.save_cart()
        
    def decrement_product(self, product):
        product_id = str(product.id)
        if product_id in self.cart.keys():
            self.cart[product_id]["amount"] -= 1
            if self.cart[product_id]["amount"] <= 0:
                self.delete_product(product)
        self.save_cart()
        
    def delete_product(self, product):
        product_id = str(product.id)
        if product_id in self.cart.keys():
            del self.cart[product_id]
            self.seve_cart()
        
    def delete_cart(self):
        self.sesion["cart"] = {}
        self.sesion.modified = True