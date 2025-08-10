from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Products, Category, WishList,Bander, Rating, Comment_product
from django.views.generic.list import ListView
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from django import template
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.contrib.contenttypes.models import ContentType
from .forms import RatingForm, Comment_Form
from django.db.models import Avg


def get_products(request):
    products = Products.objects.filter(especial=True, active=True).annotate(avg_rating=Avg('ratings__stars'))
    products_cloths = Products.objects.filter(category__name="لباس", active=True).annotate(avg_rating=Avg('ratings__stars'))
    products_mode = Products.objects.filter(category__name="ارایشی بهداشتی", active=True).annotate(avg_rating=Avg('ratings__stars'))
    baner = Bander.objects.all()
    
    context={
        "product_mode": products_mode,
        "products_cloths":products_cloths,
        "products":products,
        "baner" : baner
    }
    return render(request, "shop/home.html", context)

def product(request, pk):
    user_rating = None
    comment_form = Comment_Form()
    full_sale = Products.objects.filter(full_sale=True, active=True)
    product = get_object_or_404(Products, id=pk, active=True)
    comment_product = Comment_product.objects.filter(product=product).all()
    realyted_product = Products.objects.filter(category=product.category).annotate(avg_rating=Avg('ratings__stars'))
    especial_product = Products.objects.filter(especial=True, active=True)
    # Calculate average rating
    average_rating = product.ratings.aggregate(Avg('stars'))['stars__avg'] or 0
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            rating, created = Rating.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={'stars': form.cleaned_data['stars']}
            )
            return redirect('product', pk=product.id)
    else:
        form = RatingForm()
    return render(request, 'shop/product.html', {
        'product': product,
        'form': form,
        'average_rating': round(average_rating, 1) if average_rating else 0,
        "full_sale" : full_sale,
        "especial_product" : especial_product,
        "realyted_product" : realyted_product,
        "user_rating" : user_rating,
        "comment_form" : comment_form,
        "comments" : comment_product
    })

def category(request, cat):
        cat = cat.replace("-", " ")
        category = get_object_or_404(Category, name=cat)
        products = Products.objects.filter(category=category, active=True).annotate(avg_rating=Avg('ratings__stars'))
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
        return render(request, "shop/category.html", context)
    
class Search(ListView): 
    template_name = "shop/search.html"
    paginate_by = 12
    def get_queryset(self):
        query = self.request.GET.get("q")
        if query is not None :
            return Products.objects.search_product(query).annotate(avg_rating=Avg('ratings__stars'))
        return Products.objects.filter(active=True).annotate(avg_rating=Avg('ratings__stars'))
    
def add_wishlist(request, id):
    if request.method == "POST":
        product = Products.objects.get(id=id)
        if request.user.is_authenticated:
            WishList.objects.get_or_create(
            user=request.user,
            product=product
            )
        else:     
            WishList.objects.get_or_create(
                product=product
                )
        messages.success(request, ("این محصول به لیست ارزوها اضافه شد"))             
    return redirect("get_products")
    
def add_wishlist_product(request):
   if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = Products.objects.get(id=product_id)
        if request.user.is_authenticated:
            WishList.objects.get_or_create(
            user=request.user,
            product=product
            )
        else:     
            WishList.objects.get_or_create(
                product=product
                )
        messages.success(request, ("این محصول به لیست ارزوها اضافه شد"))
        response = JsonResponse({})
        return response           

def wishlist(request):
      if request.user.is_authenticated:
         wishlist = WishList.objects.filter(user=request.user).all()
         return render(request, "wishlist.html", {"wishlist" : wishlist}) 
      wishlist = WishList.objects.all()   
      return render(request, "shop/wishlist.html", {"wishlist" : wishlist})

def comment_product (request, id):
    form = Comment_Form(request.POST)
    product = Products.objects.filter(id=id).first()
    if request.method == "POST":
      if form.is_valid():
        name = form.cleaned_data['name']
        description = form.cleaned_data['description']
        comment = Comment_product.objects.create(user=request.user, product=product, name=name, description=description)
        comment.save()
        return redirect('product', id)
      else:
          return messages.error(request, "فرم معتبر نیست")
       


