from django.conf import settings
from products.models import Product
from cart.forms import CartAddProductForm
from decimal import Decimal
import copy
class Cart:

    def __init__(self,http_request):
    
        if settings.CART_SESSION_ID not in http_request.session:
            http_request.session[settings.CART_SESSION_ID] = {}
    
        self.session = http_request.session
        self.cart = self.session[settings.CART_SESSION_ID]
    
    def __iter__(self):
        cart = copy.deepcopy(self.cart)
        products = Product.objects.filter(id__in=cart)
        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["quantity"] * item["price"]
            item["update_quantity_form"] = CartAddProductForm(
                initial={"quantity": item["quantity"], "override": True}
            )

            yield item
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def save(self):
        self.session.modified = True

    def add(self,product:Product,quantity=1,override_quantity=False):
        
        product_id = str(product.id)
        
        if not self.cart.get(product_id):

            self.cart[product_id] = {
                "quantity": 0, "price": str(product.price)
            }
        
        if override_quantity:
            quantity_update = quantity
        
        else: 
            quantity_update = self.cart[product_id]["quantity"] + quantity
        
        self.cart[product_id] = {
            "quantity": quantity_update,
            "price": str(product.price)
        }

        self.cart[product_id]["quantity"] = min(20, self.cart[product_id]["quantity"])
        
        self.save()
    
    def remove(self,product:Product):
        
        product_id = str(product.id)

        if self.cart.get(product_id):
            del self.cart[product_id]
            self.save()
    
    def get_total_price(self):
        return sum( Decimal(item['price']) * item['quantity'] for item in self.cart.values())