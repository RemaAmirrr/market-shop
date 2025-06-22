from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import LoginForm, RegisterForm, UserUpdateForm
from cart.forms import ShippingForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import ShippingPayment


def log_in(request):
    login_form = LoginForm(request.POST or None)
    print(request.user.is_authenticated)
    if login_form.is_valid():
        username = login_form.cleaned_data.get("username")
        password = login_form.cleaned_data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, ("کاربر وارد شد"))
            return redirect ("get_products")
        else:
            return redirect ("log_in")
            messages.success(request, ("مشکلی در  ورود پیش امده است"))

    context = {
       
        "login_form" : login_form,
    }    
    return render(request, "auth/log_in.html", context)   

user = get_user_model()
def register(request):
    register_form = RegisterForm(request.POST or None)

    if register_form.is_valid():
       username = register_form.cleaned_data.get("username")
       email = register_form.cleaned_data.get("email")
       password = register_form.cleaned_data.get("password")
       user.objects.create_user(username=username, email=email, password=password)  
    #    User = user.objects.filter(username=username, password=password)
    #    if User:
    #         print("========================================")
    #         login(request, User)
    #         return redirect("home")     
    context = {
             "register_form" : register_form
         }
    return render(request, "auth/register.html", context)

def log_out(request):
    logout(request)
    return redirect("log_in")

@login_required(login_url="/login")
def profile_setting(request):
    user_id = request.user.id
    profile = Profile.objects.get(user__id=user_id)
    shippingpayment = ShippingPayment.objects.get(user__id=user_id)
    form = UserUpdateForm(request.POST or None, initial={"firstname":user.first_name, "lastname":user.last_name})
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance = profile)
        shipping_form = ShippingForm(request.POST,  instance = shippingpayment)
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, 'اصلاعات پروفایل شما ویرایش شد')
            return redirect('get_products')
    else:
        shipping_form = ShippingForm( instance = shippingpayment)
        form = UserUpdateForm( instance = profile)
                
    context = {
       "shipping_form":shipping_form,
        "form_data": form,
        "form_image": profile.image
    }
    return render(request, 'profile/profile_setting.html', context)

@login_required(login_url="/login")
def profile_sidebar(request):
    context = {}
    return render(request, "profile/profile_sidebar.html", context)

@login_required(login_url="/login")
def profile_panel(request):
    context = {}
    return render(request, "profile/profile_panel.html", context)

@login_required(login_url="/login")
def profile_order(request):
    context = {}
    return render(request, "profile/profile_order.html", context)



