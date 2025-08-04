from django.shortcuts import render, get_object_or_404, redirect, reverse
from .cart import Cart
from shop.models import Products, WishList
from django.http import JsonResponse
from django.contrib import messages
from .models import Coupon, FinalModel
from .forms import CouponForm
from decimal import Decimal
from authentication.forms import UserUpdateForm
from authentication.models import Profile
from django.contrib.auth.models import User 
from cart.forms import FinalForm, InputForm, CouponForm
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from shop.models import Products
from django.conf import settings

@login_required
def checkout(request, realy_price):
   cart = Cart(request)
   profile = get_object_or_404(Profile, user__id=request.user.id)
   order = Order()   
   order.total_price=realy_price
   coupon = Coupon.objects.first()
   coupon.use = False
   coupon.save() 
   order.user=request.user
   order.save()
   if request.method == "GET":
      initial_data = {'full_name': profile.full_name, 'phone' : profile.phone,
    'email' : profile.email, 'address' : profile.address,
    'city' : profile.city, 'state' : profile.state,
    'zip_code' : profile.zipcode,'order_id': order.id, 'user': request.user}
      order_form = FinalForm(initial=initial_data)     
   order = Order.objects.get(id=order.id)
   cart.price_conunt(order)
   orderitem = OrderItem.objects.filter(order=order).all()
   del request.session['cart']
   request.session.modified = True     
   request.session['order_id'] = order.id          
   return render (request, "checkout.html", {"order_form" : order_form, "order" : order,
   "realy_price" : realy_price, "orderitem" : orderitem})

@login_required
def payedview(request):
   order_id = request.session.get('order_id')  
   order = Order.objects.get(id=order_id)
   order_item = OrderItem.objects.filter(order=order).all()
   final_form = FinalForm(request.POST or None)
   if request.method == "POST":
     
      if final_form.is_valid():
         final_form.save()
         order = Order.objects.get(id=order_id) 
         order.finaled = True
         order.save()
         total_price = order.total_price
         
         messages.success(request, 'دزخواست  خرید شما ثبت و در حال برسی است برای پرداخت و اتمام خرید در منوبار تب پیگیری سفارش را دنبال کنید ')
         return render (request, "orderitem.html", {"total_price" : total_price, "order_item" : order_item})
   else:
       return render(request, "orderitem.html", {}) 
       
@login_required
def review(request):         
   order_id = request.session.get('order_id')
   context = {}
   if order_id != None:
        order = Order.objects.filter(id=order_id).first()
        order_item = OrderItem.objects.filter(order=order).all()
        if order.finaled != True:
                profile = get_object_or_404(Profile, user=request.user)
                initial_data = {'full_name': profile.full_name, 'phone' : profile.phone,
                                'email' : profile.email, 'address' : profile.address,
                                'city' : profile.city, 'state' : profile.state,
                                'zip_code' : profile.zipcode, 'order_id': order.id, 'user': request.user}
                order_form = FinalForm(initial=initial_data)
                context['orderitem'] = order_item
                context['order_form'] = order_form
                context['realy_price'] = order.total_price
                messages.success(request, 'شما سفارش را تایید نکرده اید')
                return render (request, "checkout.html", context)     
        else:
                context={"order" : order, "order_item" : order_item, "total_price" : order.total_price }
                shipping_amount = get_object_or_404(FinalModel, order_id=order_id)
                if order.payment_status == False:
                    
                    if shipping_amount.shipping_cost > 0:
                        final_price = Decimal(order.total_price) + Decimal(shipping_amount.shipping_cost)
                        context['shipping_cost'] = shipping_amount.shipping_cost
                        context['final_price'] = final_price   
                    else:
                        messages.success(request, ' پس از براورد هزینه ارسال دکمه پرداخت ظاهر شده و شما میتوانید برای پرداخت اقدام کنید سفارش شما در حال برسی است لطفا صبور باشید') 
                    return render (request, "orderitem.html", context)
                else:
                   
                    final_price = Decimal(order.total_price) + Decimal(shipping_amount.shipping_cost)
                    context['shipping_cost'] = shipping_amount.shipping_cost
                    context['final_price'] = final_price
                    context['payment_status'] = order.payment_status
                    context['send_status'] = order.send_status   
                    return render (request, "orderitem.html", context)

   else:
        messages.success(request, ' شما یا سفارشی ثبت نکرده اید یا از حساب خود خارج شده اید برای پیگری سفارش از هدر سایت حساب کاربری سفارشات را دنبال کنید' ) 
        return render (request, "orderitem.html", context)       

@login_required          
def show_items(request, item_id):
    order = Order.objects.get(id=item_id)
    order_item = OrderItem.objects.filter(order__id=item_id).all()
    shipping_price = FinalModel.objects.get(order_id=item_id)
    context={"order" : order, "order_item" : order_item, "total_price" : order.total_price,
    "shipping_cost": shipping_price.shipping_cost,}
    if shipping_price.shipping_cost > 0:
      final_price = Decimal(order.total_price) + Decimal(shipping_price.shipping_cost)
      context["final_price"] = final_price
    else:
        messages.success(request, "سفارش  شما در حال برسی است پس از تعین هزینه ارسال دکمه پرداخت ظاهر میشود و برای پرداخت اقدام کنید")  
    return render(request, "orderitem_history.html", context) 

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

def add_to_cart(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('product_qty'))
        color = request.POST.get('color_product')
        product = get_object_or_404(Products, id=product_id)
        if product.especial:
            price = product.sale_price
        else:
            price = product.price    
        cart.add(product.id, color, price, quantity)
        messages.success(request, ("این محصول به سبد خرید اضافه شد"))
        cart_qty = cart.__len__()
        # response = JsonResponse({'Product name' : product.name})
        response = JsonResponse({'qty' : cart_qty})
        return response
    
def remove_from_cart(request, id, color):
    cart = Cart(request)
    if request.method == "POST":
        cart.remove(id, color)
        messages.success(request, ("این محصولااز سبد حزف شد"))
    return redirect('cart_summery')


def update_cart(request, id, color):
    cart = Cart(request)
    if request.method == "POST":
        quantity = int(request.POST.get('quantity'))
        cart.update(id, color, quantity)
        messages.success(request, ("سبدخریداپدیت شد"))
    return redirect('cart_summery')   
 
def cart_detail(request):
    cart = Cart(request)
    coupon = Coupon.objects.first()
    all_total_price = cart.get_total_price()
    coupon_form = CouponForm(request.POST or None)
    cart_qty = cart.__len__()
    cart_items = []
    for item in cart:
        product = get_object_or_404(Products, id=item['product_id'])
        cart_items.append({
            **item,
            'product': product,
            'total_price': item['price'] * item['quantity'],
            'form' : InputForm(initial={'qty':item['quantity']})
        })
    context = {
           'cart_items': cart_items, 'coupon_form' : coupon_form,
            'all_total_price': all_total_price, 'realy_price' : all_total_price, "cart_qty" : cart_qty 
            }
         
    if request.method == "POST":
        if coupon_form.is_valid():
            code_coupon = coupon_form.cleaned_data.get('code')
            if coupon:  
                if coupon.code == code_coupon:
                    coupon.use = True
                    coupon.save()
                    messages.success(request,("کد تخفیف اعمال شد"))       
                else:
                    messages.success(request,("این کد معتبر نمی باشد"))           
            else:
                messages.success(request,("کد تخفیفی در نظر گرفته نشده است"))      
        else:
            messages.success(request,("کوپن فرم نامعتبر است"))   
    if coupon.use:
        last_number = coupon.amount
        off_price = all_total_price * Decimal(int(last_number)/100)
        realy_price = float(all_total_price-off_price)
        context['off_price'] = off_price
        context['realy_price'] = realy_price
        # messages.success(request,("کد تخفیف اعمال شده است"))    
    return render (request, "cart.html", context)
      
def add_cart_product(request, id):
    cart = Cart(request)
    if request.method == 'POST':
        product = get_object_or_404(Products, id=id)
        if product.especial == True:
            price = product.sale_price
        else:
            price = product.price 
        cart.add(id, quantity=1, price=price, color="----")
        messages.success(request, ("این محصول به سبد خرید اضافه شد"))
        return redirect(reverse('product', kwargs={'pk': id}))
    
def add_cart_home(request, id): 
    cart = Cart(request)
    if request.method == 'POST':
        product = get_object_or_404(Products, id=id)
        if product.especial == True:
            price = product.sale_price
        else:
            price = product.price 
        cart.add(id, quantity=1, price=price, color="----")
        messages.success(request, ("این محصول به سبد خرید اضافه شد"))
        return redirect('get_products') 
    
# all view for wislist    
def cart_add_wishlist(request, id):
    cart = Cart(request)
    if request.method == "POST":
        wishlist = get_object_or_404(WishList, id=id)
        if wishlist.product.especial == True:
            price = wishlist.product.sale_price
        else:
            price = wishlist.product.price 
        cart.add(int(wishlist.product.id), quantity=1, price=price, color="----")
        messages.success(request, ("این محصول به لیت ارزها اضافه شد"))
    return redirect("wishlist")         
      
def delete_wishlist (request, id):
   if request.method == "POST":
      wishlist = WishList.objects.get(id=id)
      wishlist.delete()
      messages.success(request, ("این محصول از لیست ارزوها حزف شد"))
   return redirect("wishlist")     
 
# all admin view
def show_all_order_item(request):
    context={}
    if request.method == "POST":
        id = request.POST.get('number_input')
        if id != '':
            order = Order.objects.filter(id=int(id), finaled=True).first()
            if order:
                order_item = OrderItem.objects.filter(order=order)
                context["total_price"] = order.total_price
                context['order_item'] = order_item
            else:
                context['massage'] = "سفارشی بااین ایدی پیدا نشد"
        else:
            context['massage'] = "لطفا یک ایدی وارد کنید"             
    return render(request, "show_item.html", context)



