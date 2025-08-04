from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User

admin.site.register(Profile)
# class ProfileInLine(admin.StackedInline):
#     model = Profile
# class UserAdmin(admin.ModelAdmin):
#     model = User
#     # fields = ['username', 'first_name', 'last_name', 'email']
#     fields = ['username', 'email']
#     inlines = [ProfileInLine]

# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)


# Register your models here.
