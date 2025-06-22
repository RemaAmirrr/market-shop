from django.urls import path
from . import views 



urlpatterns = [
    
   path("log_in/", views.log_in, name="log_in" ),
   path("register/", views.register, name="register"),
   path("log_out/", views.log_out, name="log_out"),
   path("profile_setting/", views.profile_setting, name="profile_setting"),
   path("profile_order",views.profile_order, name="profile_order"),
   path("profile_panel", views.profile_panel, name="profile_panel"),
   path("profile_setting", views.profile_sidebar, name="profile_sidebar"),
]