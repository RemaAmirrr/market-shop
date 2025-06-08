
from django.urls import path
from . import views 


urlpatterns = [
    
   path("", views.cart_summery, name="cart_summery"),
   path("add_cart/",views.add_cart, name="add_cart"),
   path("delete_cart/",views.delete_cart, name="delete_cart"),
   path("update_cart/",views.update_cart, name="update_cart") 

]