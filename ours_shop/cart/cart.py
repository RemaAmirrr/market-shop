from shop.models import Products

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart 

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)


        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True            

    def __len__(self):
        return len(self.cart) 
    
    def get_prods(self):
        product_ids = self.cart.keys()
        products = Products.objects.filter(id__in=product_ids)
        return products
    
    def get_quants(self):
        quantites = self.cart
        return quantites
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        ourcart = self.cart
        ourcart[product_id] = product_qty
        self.session.modified = True

        alaki = self.cart
        return alaki 
    
    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
  
    def get_total(self):
        product_id = self.cart.keys()
        products = Products.objects.filter(id__in=product_id)
        total = 0
        for key,value in self.cart.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.especial:
                        total = total + (product.sale_price*value)
                    else:
                        total = total + (product.price*value)
        return total  

    def price_conunt(self):
        product_id = self.cart.keys()
        products = Products.objects.filter(id__in=product_id)
        total=[]
        for key,value in self.cart.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.active:
                        total.append(product.price*value)
                    else:
                        total.append(product.price*value)
        return total                   