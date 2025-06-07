from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
import os
import random

def get_file_extension(file):
    base_name = os.path.basename(file)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image(instance, filename):
    rand_name = random.randint(1, 999999999999)
    name, ext = get_file_extension(filename)
    final_name = f"{instance.id}-{instance.name}-{rand_name}{ext}"
    return f"products/{final_name}"

# def gallery_upload_image(instance, filename):
#     rand_name = random.randint(1, 999999999999)
#     name, ext = get_file_extension(filename)
#     final_name = f"{instance.id}-{instance.name}-{rand_name}{ext}"
#     return f"gallery/{final_name}"

# class ProductManageObjects(models.Manager):
  
#     def get_active_object(self):
#         return self.get_queryset().filter(active=True)
    
#     def get_active_show_object(self):
#         return self.get_queryset().filter(active=False, show=False)
    
#     def get_product_by_id(self, product_id):
#         qs = self.get_queryset().filter(id=product_id, active=True)
#         if qs.count() == 1:
#             return qs.first()
#         return None

#     def search_product(self, query):
#         lookup = Q (title__icontains=query) | Q(description__icontains=query) | Q (tag__title__icontains=query)
#         return self.get_queryset().filter(lookup, active=True).distinct()
    
#     def get_product_by_category(self, category_name):
#         return self.get_queryset().filter(category__name__iexact=category_name)


class Category(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name="دسته"
        verbose_name_plural="دسته بندی"

    def __str__(self):
        return self.name

class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f'(self.first_name) (self.last_name)'
    
class Products(models.Model):
    name = models.CharField(max_length=40, verbose_name="نام")
    description = models.CharField(max_length=50, blank=True, null=True, verbose_name="شرح")
    price = models.DecimalField(default=0, decimal_places=0, max_digits=12, verbose_name="قیمت")
    sale_price = models.DecimalField(default=0, decimal_places=0, max_digits=12, verbose_name="فیمت ویژه")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, verbose_name="دستهبندی")
    picture = models.ImageField(upload_to=upload_image, verbose_name="تصویر")
    star = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    especial = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    newst = models.BooleanField(default=False)
    full_sale = models.BooleanField(default=False)
    offer = models.BooleanField(default=False)
    

    class Meta:
        verbose_name="محصول"
        verbose_name_plural="محصولات"

    def __str__(self):
        return self.name 
    
class Order(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    quantity = models.IntegerField(default=1)
    address = models.CharField(default='', max_length=400, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date = models.DateField(default=datetime.datetime.today())
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name


# Create your models here.
