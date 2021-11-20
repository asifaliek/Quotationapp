from products.models import Product


def update_quantity(pk,qty,status):
    product = Product.objects.get(pk=pk)
    stock = product.qty
    if status == "increase":
        balance_stock = stock + qty
    if status == "decrease":
        balance_stock = stock - qty
    
    product.qty = balance_stock
    product.save()