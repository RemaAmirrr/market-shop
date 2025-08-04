from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import os
import random
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


def get_file_extension(file):
    base_name = os.path.basename(file)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image(instance, filename):
    rand_name = random.randint(1, 999999999999)
    name, ext = get_file_extension(filename)
    final_name = f"{instance.id}-{instance.full_name}-{rand_name}{ext}"
    return f"profile/{final_name}"


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
    email = models.EmailField(blank=True, verbose_name="ایمیل")
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


# from django.contrib.auth.models import (
#     BaseUserManager, AbstractBaseUser
# )

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_image_filepath(self, filename):
    return 'profile/profile_images/' + str(self.pk) + '/profile_image.png'

def get_default_profile_image():
    return 'profile/profile_default/default_profile_image.png'

class Account(AbstractBaseUser):
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
    hide_email = models.BooleanField(default=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


