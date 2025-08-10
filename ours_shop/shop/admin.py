from django.contrib import admin
from . import models

class GalleryInline(admin.TabularInline):
    model = models.Gallery
    extra = 3

class SpecificationInline(admin.TabularInline):
    model = models.Specification
    extra = 3
    
class SizeinlIne(admin.TabularInline):
    model = models.Size
    extra = 3

class ColorinlIne(admin.TabularInline):
    model = models.Color
    extra = 3

class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", 'price', 'category', 'stock_qty', "active"]
    #list_editable = ['featured']
    list_filter = ['date']
    search_fields = ['name']
    inlines = [GalleryInline,  SizeinlIne, ColorinlIne]
    
admin.site.register(models.Category)
admin.site.register(models.Products, ProductAdmin)

class ReviewAdime(admin.ModelAdmin):
    list_display = ["user", "product"] 

class Wishlistadmin(admin.ModelAdmin):
    list_display=["user"]  

# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ["user", "vendor", "order"]


admin.site.register(models.Review, ReviewAdime)
admin.site.register(models.WishList, Wishlistadmin)
admin.site.register(models.Bander)
admin.site.register(models.Rating)
admin.site.register(models.Color)
admin.site.register(models.Comment_product)

# admin.site.register(models.Notification, NotificationAdmin)






