from django.shortcuts import render, get_object_or_404
from .cart import Cart
from shop.models import Products
from django.http import JsonResponse

def cart_summery(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants() 
    total = cart.get_total()
    return render (request, "cart.html", {'cart_products':cart_products, 'quantities' :  quantities, 'total' : total })


def add_cart(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Products, id=product_id)
        cart.add(product=product, quantity=product_qty)
        cart_qty = cart.__len__()

        # response = JsonResponse({'Product name' : product.name})
        response = JsonResponse({'qty' : cart_qty})
        return response

 
def cart_delete (request):
   cart = Cart(request)
   if request.POST.get('action') == 'post':
      product_id = int(request.POST.get('product_id'))
      cart.delete(product=product_id)
      response = JsonResponse({'product' : product_id})
      return response

def cart_update(request):
   cart = Cart(request)  
   if request.POST.get('action') == 'post':
      product_id = str(request.POST.get('product_id'))
      product_qty = int(request.POST.get('product_qty')) 
      cart.update(product=product_id, quantity = product_qty)
      response = JsonResponse({'qty' : product_qty})
      return response

# Create your views here.
