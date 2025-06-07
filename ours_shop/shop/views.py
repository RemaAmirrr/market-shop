from django.shortcuts import render, redirect
from .models import Products, Category


def get_products(request):
    
    products = Products.objects.filter(especial=True).all
    context={
        "products":products
    }
    return render(request, "home.html", context)

def product(request, pk):

    full_sale = Products.objects.filter(full_sale=True)
    product = Products.objects.get(id=pk)
    especial_product = Products.objects.filter(especial=True)
    
    context = {
        "product": product,
        "full_sale" : full_sale,
        "especial_product" : especial_product,
    }
    return render(request, "product.html", context)

def category(request, cat):
    cat = cat.replace("-", " ")

    try:
        category = Category.objects.get(name=cat)
        products = Products.objects.filter(category=category).all()
        especial_product = Products.objects.filter(especial=True)
        full_sale = Products.objects.filter(full_sale=True)

        context={
            "especial_product" : especial_product,
            "category" : category,
            "products" : products,
            "full_sale" : full_sale
        }
        return render(request, "category.html", context)
    except:
        return redirect ("get_products")