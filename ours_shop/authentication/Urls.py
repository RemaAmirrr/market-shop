from django.urls import path, include
from . import views 
from django.contrib.auth.views import PasswordChangeDoneView





urlpatterns = [
    
   path("log_in/", views.log_in, name="log_in" ),
   path("register/", views.register, name="register"),
   path("log_out/", views.log_out, name="log_out"),
   path("profile_setting/", views.profile_setting, name="profile_setting"),
   path("django_url/", include("django.contrib.auth.urls")),
   path('phone_verification/', views.phone_verification, name='phone_verification'),
   path('code_verification/', views.code_verification, name='code_verification'),
   path('password_reset_new/', views.password_reset_new, name='password_reset_new'),
   path(
        'change-password/',
        views.PersianPasswordChangeView.as_view(),
        name='password_change'
    ),
    path(
        'change-password/done/',
        PasswordChangeDoneView.as_view(
            template_name='auth/password_change_done.html'
        ),
        name='password_change_done'
    ),
]


  