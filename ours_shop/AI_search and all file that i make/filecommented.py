# def cart_update(request):
#    cart = Cart(request)  
#    if request.POST.get('action') == 'post':
#       product_id = str(request.POST.get('product_id'))
#       product_qty = int(request.POST.get('product_qty')) 
#       cart.update(product=product_id, quantity = product_qty)
#       messages.success(request, ("محصول اپدیت شد"))
#       response = JsonResponse({'qty' : product_qty})
#       return response

#  def payedview(request):
#    final_form = FinalForm(request.POST or None)
#    order_id = request.session.get('order_id')
#    if request.method == "POST":
#       if final_form.is_valid():
#          final_form.save()
#          order = Order.objects.get(id=order_id) 
#          order.finaled = True
#          order.save()
#          total_price = order.total_price
#          messages.success(request, 'دزخواست  خرید شما ثبت و در حال برسی است برای پرداخت و اتمام خرید در منوبار تب پیگیری سفارش را دنبال کنید ')
#          return render (request, "orderitem.html", {"total_price" : total_price, }) 
#    context = {}
#    if order_id != None: 
#         order = Order.objects.get(id=order_id)
#         orderitem = OrderItem.objects.filter(order=order).all() 
#         if order.finaled == True:
#             shipping_amount = FinalModel.objects.get(order_id=order_id)
#             if request.user.is_authenticated:
#                 profiel = Profile.objects.get(user=request.user)
#                 order.user = request.user
#                 order.save()
#                 shipping_amount.full_name = profiel.full_name
#                 shipping_amount.phone = profiel.phone
#                 shipping_amount.address1 = profiel.address1
#                 shipping_amount.address2 = profiel.address2
#                 shipping_amount.city = profiel.city
#                 shipping_amount.state = profiel.state
#                 shipping_amount.zip_code = profiel.zipcode
#                 shipping_amount.country = profiel.country
#                 shipping_amount.email = profiel.email
#                 shipping_amount.save()
#             if shipping_amount.shipping_cost > 0:
#                 final_price = Decimal(order.total_price) + Decimal(shipping_amount.shipping_cost)
#                 order_item = OrderItem.objects.filter(order=order).all()
#                 context={
#                     "order" : order,
#                     "order_item" : order_item,
#                     "final_price" : final_price,
#                     "total_price" : order.total_price,
#                     "shipping_cost" : shipping_amount.shipping_cost
#                         }
#             else:
#                 context = {"total_price" : order.total_price}
#                 messages.success(request, ' پس از براورد هزینه ارسال میتوانید برای پرداخت اقدام کنید سفارش شما در حال برسی است لطفا صبور باشید') 
#             return render (request, "orderitem.html", context)
#         else:
#            messages.success(request, 'شما سفارش را تایید نکرده اید')
#            if request.user.is_authenticated:
#                   profile = Profile.objects.get(user=request.user)
#                   initial_data = {'full_name': profile.full_name, 'phone' : profile.phone,
#                                    'email' : profile.email, 'address1' : profile.address1,
#                                     'address2' : profile.address2, 'city' : profile.city, 'state' : profile.state,
#                                     'zip_code' : profile.zipcode, 'country' : profile.country,'order_id': order.id, 'user': request.user}
#                   order_form = FinalForm(initial=initial_data)
#            else:
#                initial_data = {'order_id': order.id}
#                order_form = FinalForm(initial=initial_data)
        
#            context = {
#             "orderitem" : orderitem,
#             "order_form" : order_form
#            }
#            return render (request, "checkout.html", context)
#    else:
#         messages.success(request, ' شما سفارشی ثبت نکردید') 
#         return render (request, "orderitem.html", context)


# def checkout(request, realy_price):
#    cart = Cart(request)
#    coupon = Coupon.objects.first()
#    total = cart.get_total_price()
#    profile = get_object_or_404(Profile, user__id=request.user.id)
#    order = Order()
#    coupon_used = request.session.get('coupon_used')
#    if coupon:
#            if coupon_used == "coupon_ok":   
#                 last_number = coupon.amount
#                 off_price = total * Decimal(int(last_number)/100)
#                 realy_price = total - off_price
#                 order.total_price = realy_price
#                 if request.user.is_authenticated:
#                     order.user=request.user
#                     order.save()
#                     if request.method == "GET":
#                         initial_data = {'full_name': profile.full_name, 'phone' : profile.phone,
#                                         'email' : profile.email, 'address1' : profile.address1,
#                                             'address2' : profile.address2, 'city' : profile.city, 'state' : profile.state,
#                                             'zip_code' : profile.zipcode, 'country' : profile.country,'order_id': order.id, 'user': request.user}
#                         order_form = FinalForm(initial=initial_data)
#                 else:
#                     order.save()
#                     initial_data = {'order_id': order.id}
#                     order_form = FinalForm(initial=initial_data)     
                 
#    else:
#        order.total_price=total
#        if request.user.is_authenticated:
#                order.user=request.user
#                order.save()
#                if request.method == "GET":
#                   initial_data = {'full_name': profile.full_name, 'phone' : profile.phone,
#                                    'email' : profile.email, 'address1' : profile.address1,
#                                     'address2' : profile.address2, 'city' : profile.city, 'state' : profile.state,
#                                     'zip_code' : profile.zipcode, 'country' : profile.country,'order_id': order.id, 'user': request.user}
#                   order_form = FinalForm(initial=initial_data)
#                realy_price = total   
#        else:
#             order.save()
#             if request.method == "GET":
#                   initial_data = {'order_id': order.id}
#                   order_form = FinalForm(initial=initial_data) 
#             realy_price = total

 # email = forms.EmailField(
    #     label="ایمیل",
    #     widget=forms.EmailInput(attrs={"class" : "form-control", "placeholder" : "ایمیل خود را وارد کنید"}), validators=[
    #     validators.EmailValidator("!ایمیل نامعتبر است")
    # ])


 # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     qurey = user.objects.filter(email=email)
    #     if qurey.exists():
    #         raise forms.ValidationError("این ایمیل قبلا ثبت شده است")
    #     return email


# @login_required(login_url="/login")
# def profile_sidebar(request):
#     context = {}
#     return render(request, "profile/profile_sidebar.html", context)

# @login_required(login_url="/login")
# def profile_panel(request):
#     context = {}
#     return render(request, "profile/profile_panel.html", context)

# @login_required(login_url="/login")
# def profile_order(request):
#     context = {}
#     return render(request, "profile/profile_order.html", context)


# def search(request): if you want for run search by funcation base you can use this code but for pagination i dont get any result 
#     if request.method == 'POST':
#         searched = request.POST['searched']
#         if  searched:
#             searched = Products.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
#             paginator = Paginator(searched, 8)
#             page_number = request.GET.get("page")
#             page_obj = paginator.get_page(page_number)
#             if searched:
#                 return render(request, 'search.html', {'searched':searched, "page_obj":page_obj})  
#             else:
#                 messages.success(request, ("محصول مورد نظر پیدا نشد"))
#                 return render(request, 'search.html', {})
#         else: 
#            messages.success(request, ("برای یافتن محصول نام ان را در کادر سرچ وارد کنید"))   
#            return render(request, 'search.html', {})    

# class ProductDetailView(DetailView):
#     model = Products
#     template_name = 'product.html'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         obj = context['object']

#         product = get_object_or_404(Products, id=self.kwargs['pk'], active=True)
#         full_sale = Products.objects.filter(full_sale=True, active=True)
#         especial_product = Products.objects.filter(especial=True, active=True)
#         realyted_product = Products.objects.filter(category=product.category)
        
#         # Get user's rating
#         context['user_rating'] = get_user_rating(self.request.user, obj)
        
#         # Get content type ID for rating form
#         context['content_type_id'] = ContentType.objects.get_for_model(obj).id
        
#         # Get average rating
#         context['average_rating'] = obj.average_rating
#         context['rating_count'] = obj.rating_count
#         context['especial_product'] = especial_product
#         context['realyted_product'] = realyted_product
#         context['full_sale'] = full_sale
#         context['product'] = product
       
        
#         return context


# class RateObjectView(FormView):
#     form_class = RatingForm
#     template_name = 'rating.html'

#     def form_valid(self, form):
#         content_type = ContentType.objects.get_for_id(self.kwargs['content_type_id'])
#         rating, created = Rating.objects.update_or_create(
#             user=self.request.user,
#             content_type=content_type,
#             object_id=self.kwargs['object_id'],
#             defaults={'stars': form.cleaned_data['stars']}
#         )
#         return super().form_valid(form)
    
#     def get_success_url(self):
#         return self.content_object.get_absolute_url()

#    del request.session['cart']
#    request.session.modified = True 
#    order = Order.objects.get(id=order.id)
#    cart.price_conunt(order)
#    orderitem = OrderItem.objects.filter(order=order).all()   
#    request.session['order_id'] = order.id          
#    return render (request, "checkout.html", {"order_form" : order_form, "order" : order,
#    'total' : total, "realy_price" : realy_price, "orderitem" : orderitem})

# def cart_delete (request):
#    cart = Cart(request)
#    if request.POST.get('action') == 'post':
#       product_id = int(request.POST.get('product_id'))
#       cart.delete(product=product_id)
#       messages.success(request, ("این محصول از سبد خرید حدف شد"))
#       response = JsonResponse({'product' : product_id})
#       return response 
# 
# # def add_cart(request):
#     cart = Cart(request)
#     if request.POST.get('action') == 'post':
#         product_id = int(request.POST.get('product_id'))
#         product_qty = int(request.POST.get('product_qty'))
#         color_product = request.POST.get('color_product')
#         print("==================================",color_product)

#         product = get_object_or_404(Products, id=product_id)
#         cart.add(product=product, quantity=product_qty, color_product=color_product)
#         messages.success(request, ("این محصول به سبد خرید اضافه شد"))
#         cart_qty = cart.__len__()
#         # response = JsonResponse({'Product name' : product.name})
#         response = JsonResponse({'qty' : cart_qty})
#         return response  
# 
# 
# def cart_summery(request):
#     cart = Cart(request)
#     cart_qty = cart.__len__()
#     coupon_form = CouponForm(request.POST or None)
#     coupon = Coupon.objects.first()
#     all = cart.item_cart()
#     shared_data = request.session.get('shared_data')
#     items=[]
#     cart_products = cart.get_prods()
#     for item in cart_products:
#         for val in all:
#             if val == item:
#                 items.append({item.id : val})

# class Category(ListView):
#     model = Products
#     paginate_by = 4
#     template_name = "category.html"
#     context_object_name = 'products'

#     def get_queryset(self):
#         self.category = get_object_or_404(Category, Name=self.kwargs['cat'])
#         return Products.objects.filter(category=self.category).order_by('name')
                                                               
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['current_category'] = self.category
#         return context

#     quantities = cart.get_quants() 
#     total = cart.get_total()
#     if cart_qty > 0: 
#       if shared_data == "coupon_used":
#             last_number = coupon.amount
#             off_price = total * Decimal(int(last_number)/100)
#             realy_price = total - off_price
#             messages.success(request, ("کوپن تخفیف اعمال شده است"))
#       else: 
#          realy_price = total
#          off_price = 0
#     else:
#        realy_price = total
#        off_price = 0            
#     return render (request, "cart.html", {'cart_products':cart_products,  "coupon_form" : coupon_form, "off_price" : off_price,
#                                     'quantities' :  quantities, 'total' : total, "realy_price" : realy_price, "cart_qty" : cart_qty}) 
# 

# def header(request):
#     # setting = Setting_site.objects.first()
#     cart = Cart(request)
#     total = cart.get_total_price()
#     # Products = cart.get_prods()
#     count = cart.get_quants()
#     context = { 
#        "total": total,
#     #    "Products" : Products,
#        "count" : count
#     }
#     return render(request, "base/header.html", context)
# 
#     
 # path('category/<cat>',views.Category.as_view(), name="category"),
 # path('product/<int:pk>/', views.ProductDetailView.as_view(), name="product"),
 # path('rate/<int:content_type_id>/<int:object_id>/', views.RateObjectView.as_view(), name='rate-object'),         

# Create your views here.


# path("", views.cart_summery, name="cart_summery"),
 # path("add_cart/",views.add_cart, name="add_cart"),
 # path("cart_delete/",views.cart_delete, name="cart_delete")
# path("cart_update/",views.cart_update, name="cart_update"),
# path("coupon/", views.use_coupon, name="use_coupon"),
     
# def use_coupon (request):
#     cart = Cart(request)
#     cart_qty = cart.__len__()
#     coupon = Coupon.objects.first()
#     total__price = cart.get_total_price()
#     coupon_form = CouponForm(request.POST or None)
#     cart_items=[]
#     for item in cart:
#         product = get_object_or_404(Products, id=item['product_id'])
#         cart_items.append({**item, 'product': product, 'total_price': Decimal(item['price'] * item['quantity'])})   
#     context={"all_total_price" : float(total__price), "coupon_form" : coupon_form, "cart_items" : cart_items, "cart_qty" : cart_qty }
    
    # if coupon_form.is_valid():
    #    code_coupon = coupon_form.cleaned_data.get('code')
    #    if coupon:
    #      if cart_qty > 0:
    #         if coupon.code == code_coupon:
    #             last_number = coupon.amount
    #             off_price = total__price * Decimal(int(last_number)/100)
    #             realy_price = float(total__price-off_price)
    #             context['off_price'] = off_price
    #             context['realy_price'] = realy_price
    #             coupon = request.session.get('coupon')
    #             request.session.modified = True 
    #             messages.success(request,("کد تخفیف اعمال شد"))
    #             return render(request, "cart.html", context)   
    #         else:
    #             messages.success(request,("این کد معتبر نمی باشد"))
    #             return render(request, "cart.html", context) 
    #      else:
    #             messages.success(request,("برای اعمال کد باید سبد خرید پر باشد"))
    #             return render(request, "cart.html", context)              
    #    else:
    #         messages.success(request,("کد تخفیفی در نظر گرفته نشده است"))
    #         return render(request, "cart.html", context)
    # else:
    #     messages.success(request,("کوپن فرم نامعتبر است"))
    #     return render(request, "cart.html", context)                       

#     def price_conunt(self, order):
#         product_id = self.cart.keys()
#         products = Products.objects.filter(id__in=product_id).all()
#         one_price = []
#         for key,value in self.cart.items():
#             key = int(key)
#             for product in products:
#                 if product.id == key:
#                     if product.especial:
#                        item_price = (product.sale_price)
#                     else:
#                        item_price = (product.price)
                           
#                     OrderItem.objects.create(
#                     picture=product.picture,    
#                     order=order,
#                     product=product,
#                     quantity=value,
#                     price_at_order=item_price,
#                     all_price = (value * item_price),
#                     )
#                     add_price = (value*item_price) 
#                     one_price.append(add_price)
                    
#         return one_price 
    
         


# class Cart:
#     def __init__(self, request):
#         self.session = request.session
#         cart = self.session.get('session_key')
#         if 'session_key' not in request.session:
#             cart = self.session['session_key'] = {}
#         self.cart = cart 

#     def add(self, product, quantity, color_product):
#         product_id = str(product.id)
#         product_qty = str(quantity)
#         color_products = str(color_product)
        
#         if product_id in self.cart:
#             pass
#         else:
#             # item_price = str(product.price*product_qty)
#             self.cart[product_id] = [int(product_qty), color_products]
#             #self.cart[item_price] = int(item_price)
#         self.session.modified = True
               
#     def item_cart(self):
#         items=self.cart.items()
#         return items

#     def __len__(self):
#         return len(self.cart) 
    
#     def get_prods(self):
#         product_ids = self.cart.keys()
#         products = Products.objects.filter(id__in=product_ids)
#         # colors = self.cart.values()
        
#         return products
    
#     def get_quants(self):
#         quantites = self.cart
#         return quantites
    
#     def update(self, product, quantity):
#         product_id = str(product)
#         product_qty = int(quantity)
#         ourcart = self.cart
#         ourcart[product_id] = product_qty
#         self.session.modified = True

#         alaki = self.cart
#         return alaki 
    
#     def delete(self, product):
#         product_id = str(product)
#         if product_id in self.cart:
#             del self.cart[product_id]
#         self.session.modified = True
  
#     def get_total(self):
#         product_id = self.cart.keys()
#         products = Products.objects.filter(id__in=product_id)
#         total = 0
#         for key,value in self.cart.items():
#             key = int(key)
#             for product in products:
#                 if product.id == key:
#                     if product.especial:
#                         total = total + (product.sale_price*value[0])
#                     else:
#                         total = total + (product.price*value[0])
#         return total  

#     def price_conunt(self, order):
#         product_id = self.cart.keys()
#         products = Products.objects.filter(id__in=product_id).all()
#         one_price = []
#         for key,value in self.cart.items():
#             key = int(key)
#             for product in products:
#                 if product.id == key:
#                     if product.especial:
#                        item_price = (product.sale_price)
#                     else:
#                        item_price = (product.price)
                           
#                     OrderItem.objects.create(
#                     picture=product.picture,    
#                     order=order,
#                     product=product,
#                     quantity=value,
#                     price_at_order=item_price,
#                     all_price = (value * item_price),
#                     )
#                     add_price = (value*item_price) 
#                     one_price.append(add_price)
                    
#         return one_price 
# 
# 
# 
# 
# 
# # 
# def forget_password(request):
#     forget_password = Forget_Password(request.POST or None)
#     if request.method == "POST":
#         if forget_password.is_valid():
#             # phone_number = forget_password.cleaned_data.get("number_phone")
#             # sms = ghasedakpack.Ghasedak(GHASEDAK_API_KEY)
#             # good_line_number_for_sending_otp = '30005088'
#             # template_name_in_ghasedak_me_site = "markt_shop"
#             # n=random.randint(100000, 999999)
#             # answer = sms.verification({'receptor' : phone_number, 'linenumber' : good_line_number_for_sending_otp, 'type' : '1', 'template': template_name_in_ghasedak_me_site,'param1' : n})
#             # if answer:
#             #     return redirect("get_code", code=n) 
#             # else:
#             #     messages(request, "ارسال پیام موفقیت امیز نبود دوباره امتحان کنید")
#             return redirect("get_code", code=123987)   
# 
# 
# 
# from django.contrib.auth.models import (
#     BaseUserManager, AbstractBaseUser
# )

# class MyAccountManager(BaseUserManager):
#     def create_user(self, email, username, password=None):
#         if not email:
#             raise ValueError('Users must have an email address')
#         if not username:
#             raise ValueError('Users must have a username')

#         user = self.model(
#             email=self.normalize_email(email),
#             username=username
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, username, password):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             password=password,
#             username=username
#         )
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user


# def get_profile_image_filepath(self, filename):
#     return 'profile/profile_images/' + str(self.pk) + '/profile_image.png'

# def get_default_profile_image():
#     return 'profile/profile_default/default_profile_image.png'

# class Account(AbstractBaseUser):
#     email = models.EmailField(max_length=60, unique=True)
#     username = models.CharField(max_length=30, unique=True)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     last_login = models.DateTimeField(auto_now=True)
#     is_admin = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
#     hide_email = models.BooleanField(default=True)


#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
#     objects = MyAccountManager()

#     def __str__(self):
#         return self.username

#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True

#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True



#         

#     else:
#         context = {"forget_password" : forget_password} 
#     return render(request, "auth/forget_password.html", context)  

# def get_code(request, code):
#     context = {"code" : code}
#     form = Get_Code_Form(request.POST or None)
#     if request.method == "POST":
#         if form.is_valid():
#             Code = form.cleaned_data.get("code")
#             if Code == code:
#                 pass
#             else: 
#                 messages.error(request, "کد وارد شده صحیح نیباشد")
#     return render(request, "get_code.html", context)        


# from django.http import HttpResponse
# from .forms import AccountAuthenticationForm, RegistrationForm, AccountUpdateForm
# from django.contrib.auth import authenticate, login, logout
# from .models import Account
# from django.conf import settings


# def login_view(request):
#     context = {}
#     user = request.user
#     if request.POST:
#         form = AccountAuthenticationForm(request.POST)
#         if form.is_valid():
#             print('form', form.cleaned_data)
#             email = form.cleaned_data.get('email')
#             raw_password = form.cleaned_data.get('password')
#             user = authenticate(email=email, password=raw_password)
#             if user:
#                 login(request, user)
#                 return redirect('account:home')
#     else:
#         form = AccountAuthenticationForm()
    
#     context['login_form'] = form
#     return render(request, 'account/login.html', context)

# def register_view(request, *args, **kwargs):
#     user = request.user
#     if user.is_authenticated:
#         return HttpResponse("You are already authenticated as " + str(user.email))
#     context = {}
#     if request.POST:
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             email = form.cleaned_data.get('email').lower()
#             raw_password = form.cleaned_data.get('password1')
#             account = authenticate(email=email, password=raw_password)
#             login(request, account)
#             destination = kwargs.get("next")
#             if destination:
#                 return redirect(destination)
#             return redirect("account:home")
#         else:
#             context['registration_form'] = form

#     else:
#         form = RegistrationForm()
#         context['registration_form'] = form
#     return render(request, 'account/register.html', context)

# def logout_view(request):
#     logout(request)
#     return redirect('account:home')

# def edit_account_view(request, *args, **kwargs):
#     if not request.user.is_authenticated:
#         return redirect('account:login')
#     user_id = kwargs.get('user_id')
#     account = Account.objects.get(pk=user_id)

#     dic = {}

#     if account.pk != request.user.pk:
#         return HttpResponse("You cannot edit this profile")
#     if request.POST:
#         form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('account:profile', user_id=account.pk)
#         else:
#             form = AccountUpdateForm(request.POST, instance=request.user,
#             initial = {
#                 'id' : account.id,
#                 'email' : account.email,
#                 'username' : account.username,
#                 'profile_image' : account.profile_image
#             }
#             )
#             dic['form'] = form

#     else:
#         form = AccountUpdateForm(
#             initial = {
#             'id' : account.id,
#             'email' : account.email,
#             'username' : account.username,
#             'profile_image' : account.profile_image
#             }
#         )
#         dic['form'] = form
#         dic['user'] = account

#     dic['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
#     return render(request, 'account/profile.html', dic) 
# 
#  path("forget_password/", views.forget_password, name="forget_password"),
#  path("get_code/", views.get_code, name="get_code"), 