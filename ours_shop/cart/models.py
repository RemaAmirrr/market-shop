from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class ShippingPayment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_fullname = models.CharField(max_length=250)
    shipping_email = models.CharField(max_length=300)
    shipping_phone = models.CharField(max_length = 25, blank=True)
    shipping_address1 = models.CharField(max_length = 250, blank=True)
    shipping_address2 = models.CharField(max_length = 250, blank=True, null=True)
    shipping_city = models.CharField(max_length = 25, blank=True)
    shipping_state = models.CharField(max_length = 25, blank=True, null=True)
    shipping_zipcode = models.CharField(max_length = 25, blank=True, null=True)
    shipping_country = models.CharField(max_length=25, default='IRAN')
    
    class Meta:
        verbose_name = "اطلاعات شخصی"
        verbose_name_plural = "مشخصات"

    def __str__(self):
        return f"{self.shipping_fullname}"
    
def createshippingpayment(sender, instance, created, **kwargs):

    if created:
        user_shippingpayment = ShippingPayment(user=instance)
        user_shippingpayment.save()

post_save.connect(createshippingpayment, sender=User)

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

    class Meta:
        verbose_name = "کوپن"
        verbose_name_plural = "کوپنها "
     
    def __str__(self):
        return self.title 
