from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import LoginForm, RegisterForm, UserUpdateForm, Forget_Password #Get_Code_Form
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# import ghasedakpack
import random

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
    context = {"login_form" : login_form,}    
    return render(request, "auth/log_in.html", context)   

user = get_user_model()
def register(request):
    register_form = RegisterForm(request.POST or None)
    if register_form.is_valid():
       username = register_form.cleaned_data.get("username")
       email = register_form.cleaned_data.get("email")
       password = register_form.cleaned_data.get("password")
       user.objects.create_user(username=username, email=email, password=password)
       account = authenticate(username=username, password=password)
       if account:
           login(request, account) 
           return redirect("get_products")       
    context = {"register_form" : register_form}
    return render(request, "auth/register.html", context)

def log_out(request):
    logout(request)
    return redirect("log_in")

@login_required(login_url="/login")
def profile_setting(request):
    user_id = request.user.id
    profile = Profile.objects.get(user__id=user_id)
    form = UserUpdateForm(request.POST or None, initial={"firstname":user.first_name, "lastname":user.last_name})
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance = profile)
        if form.is_valid():
            form.save()
            # messages.success(request, 'اصلاعات پروفایل شما ویرایش شد')
            return redirect('profile_setting')
    else:
        form = UserUpdateForm( instance = profile)           
    context = {
        "form_data": form,
        "profile": profile
    }
    return render(request, 'profile/deepseekprofile.html', context)

def forget_password(request):
    forget_password = Forget_Password(request.POST or None)
    if request.method == "POST":
        if forget_password.is_valid():
            # phone_number = forget_password.cleaned_data.get("number_phone")
            # sms = ghasedakpack.Ghasedak(GHASEDAK_API_KEY)
            # good_line_number_for_sending_otp = '30005088'
            # template_name_in_ghasedak_me_site = "markt_shop"
            # n=random.randint(100000, 999999)
            # answer = sms.verification({'receptor' : phone_number, 'linenumber' : good_line_number_for_sending_otp, 'type' : '1', 'template': template_name_in_ghasedak_me_site,'param1' : n})
            # if answer:
            #     return redirect("get_code", code=n) 
            # else:
            #     messages(request, "ارسال پیام موفقیت امیز نبود دوباره امتحان کنید")
            return redirect("get_code", code=123987)           

    else:
        context = {"forget_password" : forget_password} 
    return render(request, "auth/forget_password.html", context)  

def get_code(request, code):
    context = {"code" : code}
    form = Get_Code_Form(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            Code = form.cleaned_data.get("code")
            if Code == code:
                pass
            else: 
                messages.error(request, "کد وارد شده صحیح نیباشد")
    return render(request, "get_code.html", context)        

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


from django.http import HttpResponse
from .forms import AccountAuthenticationForm, RegistrationForm, AccountUpdateForm
from django.contrib.auth import authenticate, login, logout
from .models import Account
from django.conf import settings


def login_view(request):
    context = {}
    user = request.user
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            print('form', form.cleaned_data)
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=raw_password)
            if user:
                login(request, user)
                return redirect('account:home')
    else:
        form = AccountAuthenticationForm()
    
    context['login_form'] = form
    return render(request, 'account/login.html', context)

def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + str(user.email))
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect("account:home")
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('account:home')


# def profile_view(request, *args, **kwargs):
#     # account = request.user
#     context = {}
#     user_id = kwargs.get('user_id')
#     try:
#         account = Account.objects.get(pk=user_id)
#     except:
#         return HttpResponse('Someting went wrong')
    
#     context['user'] = account
    
#     return render(request, 'account/profile.html', context)


def edit_account_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('account:login')
    user_id = kwargs.get('user_id')
    account = Account.objects.get(pk=user_id)

    dic = {}

    if account.pk != request.user.pk:
        return HttpResponse("You cannot edit this profile")
    if request.POST:
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account:profile', user_id=account.pk)
        else:
            form = AccountUpdateForm(request.POST, instance=request.user,
            initial = {
                'id' : account.id,
                'email' : account.email,
                'username' : account.username,
                'profile_image' : account.profile_image
            }
            )
            dic['form'] = form

    else:
        form = AccountUpdateForm(
            initial = {
            'id' : account.id,
            'email' : account.email,
            'username' : account.username,
            'profile_image' : account.profile_image
            }
        )
        dic['form'] = form
        dic['user'] = account

    dic['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, 'account/profile.html', dic)



