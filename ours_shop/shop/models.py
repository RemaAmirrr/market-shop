from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q
from shortuuid.django_fields import ShortUUIDField
import datetime
import os
import random
from django.contrib.auth.models import User
from authentication.models import Profile
from cart.models import OrderItem
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models import Avg


def get_file_extension(file):
    base_name = os.path.basename(file)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image(instance, filename):
    rand_name = random.randint(1, 999999999999)
    name, ext = get_file_extension(filename)
    final_name = f"{instance.id}-{instance.name}-{rand_name}{ext}"
    return f"products/{final_name}"

def gallery_upload_image(instance, filename):
    rand_name = random.randint(1, 999999999999)
    name, ext = get_file_extension(filename)
    final_name = f"{instance.id}-{instance.name}-{rand_name}{ext}"
    return f"gallery/{final_name}"

class ProductManageObjects(models.Manager):
  
    def get_active_object(self):
        return self.get_queryset().filter(active=True)
    
    def get_active_show_object(self):
        return self.get_queryset().filter(active=False, show=False)
    
    def get_product_by_id(self, product_id):
        qs = self.get_queryset().filter(id=product_id, active=True)
        if qs.count() == 1:
            return qs.first()
        return None

    def search_product(self, query):
        lookup = Q (name__icontains=query) | Q(description__icontains=query)
        return self.get_queryset().filter(lookup, active=True).distinct()
    
    def get_product_by_category(self, category_name):
        return self.get_queryset().filter(category__name__iexact=category_name)


class Category(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name="دسته"
        verbose_name_plural="دسته بندی"

    def __str__(self):
        return self.name
    



Status = (

("0%", 0),
("10%", 10),
("20%", 20),
("30%", 30),
("50%", 50),

)      
class Products(models.Model):
    name = models.CharField(max_length=40, verbose_name="نام")
    description = models.CharField(max_length=50, blank=True, null=True, verbose_name="شرح")
    price = models.DecimalField(default=0, decimal_places=0, max_digits=12, verbose_name="قیمت ")
    sale_price = models.DecimalField(default=0, decimal_places=0, max_digits=12, verbose_name="ویژه فیمت")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, verbose_name="دستهبندی")
    picture = models.ImageField(upload_to=upload_image, verbose_name="تصویر")
    discount = models.CharField(choices=Status, max_length=20, default="0%")
    especial = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    newst = models.BooleanField(default=False)
    full_sale = models.BooleanField(default=False)
    offer = models.BooleanField(default=False)
    stock_qty = models.PositiveIntegerField(default=1)
    views = models.PositiveBigIntegerField(default=0)
    pid = ShortUUIDField(unique=True, length=10, alphabet="abcdefg12345")
    slug = models.SlugField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    objects = ProductManageObjects()
    class Meta:
        verbose_name="محصول"
        verbose_name_plural="محصولات"

    def __str__(self):
        return self.name
    
    # def product_rating(self):
    #     product_rating = Review.objects.filter(product=self).aggregate(avg_rating=models.Avg("rating"))
    #     return product_rating['avg_rating']
    
    def rating_count(self):
        return Review.objects.filter(product=self).count()
    
    def gallery(self):
        return Gallery.objects.filter(product=self)
    
    def color(self):
        return Color.objects.filter(product=self)
    
    def orders(self):
        return OrderItem.objects.filter(product=self).count()
    
    def specification(self):
        return Specification.objects.filter(product=self)
    
    def size(self):
        return Size.objects.filter(product=self)
    
    def save(self, *args, **kwargs):
        # self.rating = self.product_rating()
        if self.slug == ""  or self.slug == None: 
            self.slug = slugify(self.name)
        super(Products, self).save(*args, **kwargs)

class Rating(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    
    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicate ratings      

class Bander(models.Model):
    name = models.CharField(max_length=30, verbose_name="نام بنر")
    image = models.FileField(upload_to="baner", null=True, blank=True, verbose_name="عکس")

    def __str__(self):
        return self.name 

    class Meta:
        verbose_name_plural = "بنرها"        
    
   
class Gallery(models.Model):
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.FileField(upload_to="product",  null=True, blank=True)
    active = models.BooleanField(default=True)
    gid = ShortUUIDField(unique=True, length=10, alphabet="abcdefg12345")

    def __str__(self):
        return self.product.name
    
    class Meta:
        verbose_name_plural = "گالری"

class Specification(models.Model):
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=1000, null=True, blank=True)
    content = models.CharField(max_length=1000 ,null=True, blank=True)

    def __str__(self):
        return self.title 

class Size(models.Model):
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=1000, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=12,  null=True, blank=True) 

    def __str__(self):
        return self.name    

class Color(models.Model):
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=1000, null=True, blank=True)
    price = models.DecimalField(decimal_places=2,  max_digits=12,  null=True, blank=True) 
 
    def __str__(self):
        return self.name     
    
class Review(models.Model):

    RATING = (
        (1, "1 star"),
        (2, "2 star"),
        (3, "3 star"),
        (4, "4 star"),
        (5, "5 star"),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    review = models.TextField()
    reply = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=None, choices=RATING)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
    
    class Meta:
        verbose_name_plural = "Reviews & Rating"

    def profile(self):
        return Profile.objects.get(user=self.user)  
    
class WishList(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,  verbose_name="کاربر")
        product = models.ForeignKey("Products", on_delete=models.CASCADE, null=True, blank=True,  verbose_name="محصول")

        class Meta:
            verbose_name="محصول"
            verbose_name_plural="لیست ارزو"

        def __str__(self):
            return self.product.name 


# Create your models here.
