class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        if "cart" not in self.session:
            self.session["cart"] = {}
        self.cart = self.session["cart"]
            
    def save_cart(self):
        self.session["cart"] = self.cart
        self.session.modified = True
            
    def add_product(self, product, amount=1):
        product_id = str(product.id)
        if product_id not in self.cart.keys():
            self.cart[product_id] = {
                "product_id": product_id,
                "name": product.name,
                "price": float(product.price),
                "amount": amount,
            }
        else:
            self.cart[product_id]["amount"] += amount
        self.save_cart()
        
    def decrement_product(self, product, amount):
        product_id = str(product.id)
        if product_id in self.cart.keys():
            self.cart[product_id]["amount"] -= amount
            if self.cart[product_id]["amount"] <= 0:
                self.delete_product(product)
        self.save_cart()
        
    def delete_product(self, product):
        product_id = str(product.id)
        if product_id in self.cart.keys():
            del self.cart[product_id]
            self.save_cart()
        
    def delete_cart(self):
        self.session["cart"] = {}
        self.session.modified = True