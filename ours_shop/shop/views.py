from django.shortcuts import render, redirect, get_object_or_404
from .models import Products, Category
from django.views.generic.list import ListView
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import Http404



def get_products(request):
    
    products = Products.objects.filter(especial=True, active=True).all
    products_cloths = Products.objects.filter(category__name="cloths", active=True)
    products_mode = Products.objects.filter(category__name="makeup", active=True)
    products_baner = Products.objects.filter(name="بنر" ).all()
    beg_baner = Products.objects.filter(name="بنر بزرگ").all()
    context={
        "product_mode": products_mode,
        "products_cloths":products_cloths,
        "products":products,
        "products_baner" : products_baner,
        "beg_baner" : beg_baner
    }
    return render(request, "home.html", context)

def product(request, pk):

    full_sale = Products.objects.filter(full_sale=True, active=True)
    product = Products.objects.get(id=pk, active=True)
    especial_product = Products.objects.filter(especial=True, active=True)
    
    context = {
        "product": product,
        "full_sale" : full_sale,
        "especial_product" : especial_product,
    }
    return render(request, "product.html", context)

    
# class Category(ListView):
#     paginate_by = 4
#     template_name = "category.html"

#     def get_queryset(self):
#         category_name = self.kwargs['cat']
#         category = Category.objects.filter(name__iexact=category_name)                                                        
#         if category is None:
#             raise Http404("محصول مورد نظر پیدا نشد")
#         product = Products.objects.get_product_by_category(category_name) 
#         return product 

def category(request, cat):
    cat = cat.replace("-", " ")

    try:
        category = Category.objects.get(name=cat)
        products = Products.objects.filter(category=category).all()
        paginator = Paginator(products, 1)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        especial_product = Products.objects.filter(especial=True)
        full_sale = Products.objects.filter(full_sale=True)

        context={

            "page_obj" : page_obj,
            "especial_product" : especial_product,
            "category" : category,
            "products" : products,
            "full_sale" : full_sale
        }
        return render(request, "category.html", context)
    except:
        return redirect ("get_products")
    
    
class Search(ListView): 
    template_name = "search.html"
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get("q")
        
        if query is not None :
            return Products.objects.search_product(query)
        return Products.objects.filter(active=True)

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