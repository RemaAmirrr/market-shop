from cart.cart import Cart 
from django.shortcuts import render, get_object_or_404
from shop.models import Products
from cart.models import Coupon
from decimal import Decimal

def header(request):
    coupon = Coupon.objects.first()
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
    context = {
        'cart_items': cart_items,
        'all_total_price': all_total_price
    }
    if coupon.use:
        last_number = coupon.amount
        off_price = all_total_price * Decimal(int(last_number)/100)
        realy_price = float(all_total_price-off_price)
        context['off_price'] = off_price
        context['realy_price'] = realy_price    
    
   
    return render(request, 'base/header.html', context)

def footer(request):
    product = Products.objects.filter(category__name="بنر").all()
    context = { 
        "product" : product 
    }
    return render(request, "base/footer.html", context)

def about_us(request):
    return render(request, "base/about_us.html", {})

def contact_us(request):
    return render(request, "base/contact_us.html",{})