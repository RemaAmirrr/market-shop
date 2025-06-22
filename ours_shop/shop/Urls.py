
from django.urls import path
from . import views 


urlpatterns = [
    
   path("", views.get_products, name="get_products"),
   path("product/<int:pk>",views.product, name="product"),
   path("category/<str:cat>",views.category, name="category"),
   # path('category/<cat>',views.Category.as_view(), name="category"),
   path('search/',views.Search.as_view(), name="search"),
]