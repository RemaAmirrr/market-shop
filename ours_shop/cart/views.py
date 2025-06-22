from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from shop.models import Products
from django.http import JsonResponse
from django.contrib import messages
from .models import Coupon
from .forms import CouponForm
from decimal import Decimal

coupon_code=False
def cart_summery(request):
    cart = Cart(request)
    coupon_form = CouponForm()
    coupon = Coupon.objects.first()
    cart_products = cart.get_prods()
    quantities = cart.get_quants() 
    total = cart.get_total()
    if coupon_code == True:
         total = total * Decimal(int(coupon.amount)/100)
         print("+++++++++++++++++++++++++++++++++++++++++++++++++")
    else:
       total = total
      
            
    return render (request, "cart.html", {'cart_products':cart_products,
                                           'quantities' :  quantities, 'total' : total,
                                             "coupon_form": coupon_form, "coupon_code": coupon_code })

def add_cart(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Products, id=product_id)
        cart.add(product=product, quantity=product_qty)
        messages.success(request, ("این محصول به سبد خرید اضافه شد"))
        cart_qty = cart.__len__()

        # response = JsonResponse({'Product name' : product.name})
        response = JsonResponse({'qty' : cart_qty})
        return response

def cart_delete (request):
   cart = Cart(request)
   if request.POST.get('action') == 'post':
      product_id = int(request.POST.get('product_id'))
      cart.delete(product=product_id)
      messages.success(request, ("این محصول از سبد خرید حدف شد"))
      response = JsonResponse({'product' : product_id})
      return response

def cart_update(request):
   cart = Cart(request)  
   if request.POST.get('action') == 'post':
      product_id = str(request.POST.get('product_id'))
      product_qty = int(request.POST.get('product_qty')) 
      cart.update(product=product_id, quantity = product_qty)
      messages.success(request, ("محصول اپدیت شد"))
      response = JsonResponse({'qty' : product_qty})
      return response
   
def use_coupon (request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants() 
    coupon = Coupon.objects.first()
    total_price = cart.get_total()
    coupon_form = CouponForm(request.POST or None)
    
    context={}
    if coupon_form.is_valid():
       print("============================================================================") 
       code_coupon = coupon_form.cleaned_data.get('code')
       if coupon:
         if coupon.code == code_coupon:
            last_number = coupon.amount
            realy_price = total_price * Decimal(int(last_number)/100)
            context["total"] = realy_price
            context["coupon_form"] = coupon_form
            context["quantities"] = quantities
            context["cart_products"] = cart_products
            coupon_code = True
            messages.success(request,("کد تخفیف اعمال شد"))
            return render(request, "cart.html", context) 
         else:
           messages.success(request,("این کد معتبر نمی باشد"))
           context["total"] = total_price
           context["coupon_form"] = coupon_form
           context["quantities"] = quantities
           context["cart_products"] = cart_products  
           return render(request, "cart.html", context) 
             
    else:
     return redirect ("cart_summery")    

# Create your views here.
