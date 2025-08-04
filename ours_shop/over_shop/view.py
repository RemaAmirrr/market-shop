from cart.cart import Cart 
from django.shortcuts import render, get_object_or_404
from shop.models import Products

def header(request):
    cart = Cart(request)
    cart_items = []
    for item in cart:
        product = get_object_or_404(Products, id=item['product_id'])
        cart_items.append({
            **item,
            'product': product,
            'total_price': item['price'] * item['quantity'],  
        })
    
    all_total_price = cart.get_total_price()
    return render(request, 'base/header.html', {
        'cart_items': cart_items,
        'all_total_price': all_total_price
    })

def footer(request):
    product = Products.objects.filter(category__name="بنر").all()
    context = { 
        "product" : product 
    }
    return render(request, "base/footer.html", context)

def about_us(request):
    return render(request, "about_us.html", {})

def contact_us(request):
    return render(request, "contact_us.html",{})