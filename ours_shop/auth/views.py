from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import LoginForm, RegisterForm

def log_in(request):

    login_form = LoginForm(request.POST or None)
    print(request.user.is_authenticated)
    if login_form.is_valid():
        username = login_form.cleaned_data.get("username")
        password = login_form.cleaned_data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect ("get_products")
        else:
            print("کاربری با این مشخصات پیدا نشد")

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
    return redirect("login")

