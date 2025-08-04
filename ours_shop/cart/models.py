from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import os
import random


Status = (

("0","0%"),
("10", "10%"),
("20", "20%"),
("30", "30%"),
("50", "50%"),

)   

class Coupon(models.Model):

    title = models.CharField(max_length=20, verbose_name="کوپن")
    code = models.CharField(max_length=20, verbose_name="کد تخفیف")
    amount = models.CharField(max_length=20, choices=Status, default=0)
    use = models.BooleanField(default=False)

    class Meta:
        verbose_name = "کوپن"
        verbose_name_plural = "کوپنها "
     
    def __str__(self):
        return str(self.title)
    

CHOISE_PIMENT = [     
    ('1', ' درگاه بانک ملت'),
    ('2', 'درگاه زرین پال'),
    ('3', 'درگاه بانک پاسارگاد'),
    ('4', 'هنگام دریافت'),
] 

CHOISE_WAY = [     
    ('1', 'تی باکس'),
    ('2', 'پست'),
    ('3', 'چاپار'),
    ('4', 'باربری'),
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,  verbose_name=" کاربری")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="ساخته شده در")
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name="اپدید شده در")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,  verbose_name="قیمت ")
    payment_status = models.BooleanField(default=False, verbose_name="وضعیت پرداخت")
    send_status = models.BooleanField(default=False, verbose_name="وضعیت ارسال")
    finaled = models.BooleanField(default=False, verbose_name="نهای شده")
    # Add other order-related fields like status, shipping address, etc.

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"

    def __str__(self):
        return f"Order {self.id} by {self.user.username if self.user else 'Guest'}"
    
def get_file_extension(file):
    base_name = os.path.basename(file)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image(instance, filename):
    rand_name = random.randint(1, 999999999999)
    name, ext = get_file_extension(filename)
    final_name = f"{instance.id}-{instance.name}-{rand_name}{ext}"
    return f"OrderItem/{final_name}"    

class OrderItem(models.Model):
    picture = models.ImageField(upload_to=upload_image, verbose_name="تصویر", default="") 
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='items')
    product = models.ForeignKey('shop.Products', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2) # Price at the time of order
    all_price = models.DecimalField(max_digits=10, decimal_places=2, default=0) # Price at the time of order

    class Meta:
        verbose_name = "مقدار"
        verbose_name_plural = " سفارش"

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'Deleted Product'}"
    
class FinalModel(models.Model):

        user = models.CharField(max_length=40, blank=True, null=True, verbose_name="کاربر")
        order_id = models.IntegerField(blank=True, null=True, verbose_name="اید سفارش")
        full_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="نام کامل")
        phone = models.CharField(max_length=40,  blank=True, null=True, verbose_name="شماره تماس")
        email = models.EmailField( blank=True, null=True, verbose_name="ایمیل")
        address = models.TextField(max_length=1000, blank=True, null=True, verbose_name='ادرس')
        city = models.CharField(max_length=100, blank=True, null=True,verbose_name="نام شهر")
        state = models.CharField(max_length=100,  blank=True, null=True,verbose_name="نام استان")
        zip_code = models.CharField(max_length=100,  blank=True, null=True, verbose_name="کدپستی")
        pay_way = models.CharField(choices=CHOISE_PIMENT, max_length=40, verbose_name="روش پرداخت")
        payed_way = models.CharField(choices=CHOISE_WAY, max_length=40, verbose_name="روش ارسال")
        shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True,verbose_name="هزینه پست")
        description = models.TextField(max_length=2000, blank=True, null=True, verbose_name="توضیحات")

        class Meta:
            verbose_name = "نهای"
            verbose_name_plural = "نهایی"
     
        def __str__(self):
            return self.full_name

