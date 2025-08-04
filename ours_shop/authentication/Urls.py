from django.urls import path, include
from . import views 
from django.contrib.auth import views as auth_views





urlpatterns = [
    
   path("log_in/", views.log_in, name="log_in" ),
   path("register/", views.register, name="register"),
   path("log_out/", views.log_out, name="log_out"),
   path("profile_setting/", views.profile_setting, name="profile_setting"),
   path("profile_order",views.profile_order, name="profile_order"),
   path("profile_panel", views.profile_panel, name="profile_panel"),
   path("profile_setting", views.profile_sidebar, name="profile_sidebar"),
   path("forget_password/", views.forget_password, name="forget_password"),
   path("get_code/", views.get_code, name="get_code"),
   path("django_url/", include("django.contrib.auth.urls")),
 

   path('change-password/', 
         auth_views.PasswordChangeView.as_view(
             template_name='password_change_form.html',
             success_url='/authentication/change-password/done/'
         ), 
         name='password_change'),
    
   path('change-password/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='password_change_done.html'
         ),
         name='password_change_done'),
]