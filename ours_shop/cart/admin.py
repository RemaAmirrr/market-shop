from django.contrib import admin
from .models import  FinalModel, Coupon,  Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    readonly_fields  = ('created_at', 'updated_at')
    ordering = ('-created_at',)

class OrderInline(admin.TabularInline):
    list_display = []

class OrderItemInline(admin.TabularInline):
    list_display = []  

class CoponAdmin(admin.ModelAdmin):
    list_display = ['title' ] 

admin.site.register(Coupon, CoponAdmin)
admin.site.register(FinalModel)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)



