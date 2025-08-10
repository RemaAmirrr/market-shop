from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import LoginForm, RegisterForm, UserUpdateForm, Forget_Password #Get_Code_Form
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PasswordResetCode
from .forms import PhoneVerificationForm, CodeVerificationForm, PersianSetPasswordForm, PersianPasswordChangeForm
from .utils import send_sms  # Implement SMS sending function
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
import random

User = get_user_model()

def log_in(request):
    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        phone = login_form.cleaned_data.get("phone")
        password = login_form.cleaned_data.get("password")
        user = authenticate(request, username=phone, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("کاربر وارد شد"))
            return redirect ("get_products")
        else:
            
            messages.success(request, ("پسورد یا شماره موبایل درست نیست"))
            return redirect ("log_in")
            
    context = {"login_form" : login_form,}    
    return render(request, "auth/log_in.html", context)   

user = get_user_model()
def register(request):
    register_form = RegisterForm(request.POST or None)
    if register_form.is_valid():
       phone = register_form.cleaned_data.get("phone")
       password = register_form.cleaned_data.get("password")
       user.objects.create_user(username=phone, password=password)
       account = authenticate(username=phone, password=password)
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
    return render(request, 'auth/deepseekprofile.html', context)


def phone_verification(request):
    if request.method == 'POST':
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            
            # Check if user exists
            if not user.objects.filter(username=phone).exists():
                messages.error(request, "شماره تلفن ثبت نشده است")
                return render(request, 'auth/phone_verification.html', {
                    'form': form,
                    'step': 1,
                    'progress_percent': 0
                })
            
            # Generate and save code
            code = ''.join(random.choices('0123456789', k=6))
            print("==============================================",code)
            PasswordResetCode.objects.filter(phone=phone).delete()  # Remove old codes
            reset_code = PasswordResetCode(phone=phone, code=code)
            reset_code.save()
            
            # In a real app, you would send the SMS here
            # send_sms(to=phone, body=f"کد تایید شما: {code}")  # we not register in gasdak site 
            print(f"DEBUG: Verification code for {phone}: {code}")
            
            request.session['reset_phone'] = phone
            return redirect('code_verification')
    else:
        form = PhoneVerificationForm()
    
    return render(request, 'auth/phone_verification.html', {
        'form': form,
        'step': 1,
        'progress_percent': 0
    })

def code_verification(request):
    phone = request.session.get('reset_phone')
    if not phone:
        return redirect('phone_verification')
    
    if request.method == 'POST':
        form = CodeVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                reset_code = PasswordResetCode.objects.get(
                    phone=phone, 
                    code=code,
                    is_used=False
                )
                if reset_code.is_valid():
                    reset_code.is_used = True
                    reset_code.save()
                    request.session['verified'] = True
                    return redirect('password_reset_new')
                else:
                    messages.error(request, "کد منقضی شده است")
            except PasswordResetCode.DoesNotExist:
                messages.error(request, "کد وارد شده نامعتبر است")
    else:
        form = CodeVerificationForm()
    
    return render(request, 'auth/phone_verification.html', {
        'form': form,
        'step': 2,
        'phone': phone,
        'progress_percent': 50
    })

def password_reset_new(request):
    if not request.session.get('verified') or not request.session.get('reset_phone'):
        return redirect('phone_verification')
    
    phone = request.session['reset_phone']
    try:
        user = User.objects.get(username=phone)
    except Profile.DoesNotExist:
        messages.error(request, "کاربر یافت نشد")
        return redirect('phone_verification')
    
    if request.method == 'POST':
        form = PersianSetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            
            # Cleanup session
            del request.session['reset_phone']
            del request.session['verified']
            
            messages.success(request, "رمز عبور با موفقیت تغییر یافت!")
            return redirect('log_in')
    else:
        form = PersianSetPasswordForm(user)
    
    return render(request, 'auth/phone_verification.html', {
        'form': form,
        'step': 3,
        'progress_percent': 100
    })

class PersianPasswordChangeView(PasswordChangeView):
    form_class = PersianPasswordChangeForm
    template_name = 'auth/password_change.html'
    success_url = reverse_lazy('password_change_done')


