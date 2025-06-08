from cart.cart import Cart 
from django.shortcuts import render


def header(request):
    cart = Cart(request)
    cart_products = cart.get_prads()
    context = {
       'cart_products' : cart_products
    }
    return render(request, "base/header.html", context)

def footer(request):
    context = {
       
    }
    return render(request, "base/footer.html", context)

def about_us(request):
    return render(request, "about_us.html", {})

def contact_us(request):
    return render(request, "contact_us.html",{})