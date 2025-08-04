
from django.urls import path
from . import views 

urlpatterns = [
    
   path('', views.cart_detail, name='cart_summery'),
   path('add/', views.add_to_cart, name='add_cart'),
   path('remove/<int:id>, <str:color>/', views.remove_from_cart, name='cart_delete'),
   path('update/<int:id>, <str:color>/', views.update_cart, name='cart_update'),
   path("add_cart_product/<int:id>/",views.add_cart_product, name="add_cart_product"),
   path("add_cart_home/<int:id>/",views.add_cart_home, name="add_cart_home"),
   
   path("check_out/<str:realy_price>/",views.checkout, name="check_out"),
   path("payed/", views.payedview, name="payed"),
   path("review/", views.review, name="review"),
   path("show_items/<int:item_id>/", views.show_items, name="show_items"),
   path("order_history/", views.order_history, name="order_history"),
   path("show_all_order_item/", views.show_all_order_item, name="show_all_order_item"),
   

   path("cart_add_wishlist/<int:id>/", views.cart_add_wishlist, name="cart_add_wishlist"),
   path("delete_wishlist/<int:id>/", views.delete_wishlist, name="delete_wishlist"),
  
]


    
    
    
    