
from django.urls import path
from . import views 


urlpatterns = [
    
   path("", views.cart_summery, name="cart_summery"),
   path("add_cart/",views.add_cart, name="add_cart"),
   path("cart_delete/",views.cart_delete, name="cart_delete"),
   path("cart_update/",views.cart_update, name="cart_update") 

]