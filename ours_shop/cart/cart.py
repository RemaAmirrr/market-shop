from shop.models import Products
from .models import  OrderItem
from decimal import Decimal
from django.shortcuts import  get_object_or_404


# myapp/cart.py
from decimal import Decimal

class Cart:
    def __init__(self, request):
        self.session = request.session
        # cart = self.session.get('cart', {})
        cart = self.session.get('cart')
        if 'cart' not in request.session:
            cart = self.session['cart'] = {}
        self.cart = cart

    def update(self, product_id, color, quantity):
        key = f"{product_id}_{color}"
        if key in self.cart:
            self.cart[key]['quantity'] = quantity
            self.save()
            return True
        return False

    def remove(self, product_id, color):
        key = f"{product_id}_{color}"
        if key in self.cart:
            del self.cart[key]
            self.save()
            return True
        return False

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def __iter__(self):
        for key, item in self.cart.items():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_quants(self):
        quantites = self.cart
        return quantites
    
    def item_cart(self):
        items=self.cart.items()
        return items
    
    def add(self, product_id, color, price, quantity=1):
        key = f"{product_id}_{color}"
        price = Decimal(price)
        
        if key in self.cart and self.cart[key]['color'] == color:
            self.cart[key]['quantity'] += quantity
        else:
            self.cart[key] = {
                'product_id': product_id,
                'color': color,
                'price': str(price),  # Store as string for serialization
                'quantity': quantity,
            }
        self.save()  

    def price_conunt(self, order):
       
        for key,value in self.cart.items():
                product = get_object_or_404(Products, id=value['product_id'])
                if product.especial:
                    item_price = (product.sale_price)
                else:
                    item_price = (product.price)     
                OrderItem.objects.create(
                picture=product.picture,    
                order=order,
                product=product,
                quantity=value['quantity'],
                price_at_order=item_price,
                all_price = (value['quantity'] * item_price),)

                 