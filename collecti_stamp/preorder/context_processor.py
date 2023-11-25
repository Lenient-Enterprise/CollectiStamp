def total_cart(request):
    total = 0
    if "cart" in request.session and request.session["cart"]:
        for key, value in request.session["cart"].items():
            total += float(value["price"]) * value["amount"]
        return {"total_cart": total}
    else:
        return {"total_cart": 0}