from django.shortcuts import render
from .models import Product

def get_products(request):
    
    products = Product.objects.filter(especial=True).all
    context={
        "products":products
    }
    return render(request, "home.html", context)

def product(request, pk):
    
    product = Product.objects.get(id=pk)
    context = {
        "product": product
    }
    return render(request, "product.html", context)