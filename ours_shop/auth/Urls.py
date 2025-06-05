from django.urls import path
from .views import log_in, log_out, register



urlpatterns = [
    
   path("log_in/", log_in, name="log_in" ),
   path("register/", register, name="register"),
   path("log_out/", log_out, name="log_out"),
]