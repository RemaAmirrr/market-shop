from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import os
import random
from django.utils import timezone
import datetime


def get_file_extension(file):
    base_name = os.path.basename(file)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image(instance, filename):
    rand_name = random.randint(1, 999999999999)
    name, ext = get_file_extension(filename)
    final_name = f"{instance.id}-{instance.full_name}-{rand_name}{ext}"
    return f"profile/{final_name}"

class PasswordResetCode(models.Model):
    phone = models.CharField(max_length=20)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:  # Set expiration only on creation
            self.expires_at = timezone.now() + datetime.timedelta(minutes=10)
        super().save(*args, **kwargs)

    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at

class Profile(models.Model):
    image = models.ImageField(upload_to=upload_image, null=True, blank=True, verbose_name="عکس")
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="نام کاربری")
    date_modefied = models.DateTimeField(User, auto_now = True)
    full_name = models.CharField(max_length=200, blank=True, verbose_name="نام کامل")
    phone = models.CharField(max_length=250, blank=True, verbose_name="تلفن")
    address = models.CharField(max_length=250, blank=True, verbose_name="ادرس")
    city = models.CharField(max_length=25, blank=True, verbose_name="شهر")
    state = models.CharField(max_length=25, blank=True, verbose_name="استان")
    zipcode = models.CharField(max_length=25, blank=True, verbose_name="")
    email = models.EmailField(blank=True,  verbose_name="ایمیل")
    description = models.TextField(max_length=2000, blank=True, null=True, verbose_name="شرح")

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name="پروفایل"
        verbose_name_plural="پروفایلها"
            
def create_profile(sender, instance, created, **kwargs):

    if created:
        user_profile = Profile(user=instance)
        user_profile.save()  

post_save.connect(create_profile, sender=User)


