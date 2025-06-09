from cart.cart import Cart 
from django.shortcuts import render


def header(request):

    # setting = Setting_site.objects.first()
    cart = Cart(request)
    total = cart.get_total()
    Products = cart.get_prods()
    count = cart.get_quants()
    context = {
    #    "setting" : setting,
       "total": total,
       "Products" : Products,
       "count" : count
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