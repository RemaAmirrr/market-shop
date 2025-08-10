
from django.urls import path
from . import views 

urlpatterns = [
    
   path("", views.get_products, name="get_products"),
   path("product/<int:pk>/",views.product, name="product"),
   path("category/<str:cat>/",views.category, name="category"),
   # path("category/<str:cat>/", views.Category.as_view(), name="category"),
   path("add_wishlist/<int:id>", views.add_wishlist, name="add_wishlist"),
   path("add_wishlist_product/", views.add_wishlist_product, name="add_wishlist_product"),
   path("wishlist/",views.wishlist, name="wishlist"),
   path('search/',views.Search.as_view(), name="search"),
   path('comment_product/<int:id>/', views.comment_product, name="comment_product")
  
]

