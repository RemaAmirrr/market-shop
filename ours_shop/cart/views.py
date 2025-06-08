from django.shortcuts import render, get_object_or_404
from .cart import Cart
from shop.models import Products
from django.http import JsonResponse

def cart_summery(request):
    cart = Cart(request)
    cart_products = cart.get_prads()
    return render (request, "cart.html", {'cart_products':cart_products})



def add_cart(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Products, id=product_id)
        cart.add(product=product)
        cart_qty = cart.__len__()

        # response = JsonResponse({'Product name' : product.name})
        response = JsonResponse({'qty' : cart_qty})
        return response


def delete_cart(request):
    return render(request, "cart.html", {})

def update_cart(request):
    return render(request, "cart.html", {})

# Create your views here.
