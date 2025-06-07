from django.shortcuts import render

def cart_summery(request):
    return render (request, "cart.html", {})

def add_cart(request):
    return render(request, "cart.html", {})

def delete_cart(request):
    return render(request, "cart.html", {})

def update_cart(request):
    return render(request, "cart.html", {})

# Create your views here.
