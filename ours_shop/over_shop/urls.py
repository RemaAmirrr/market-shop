"""
URL configuration for over_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .view import header, footer, about_us, contact_us

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("shop.Urls"), name="shop"),
    path('authentication/', include("authentication.Urls"), name="authentication"),
    path('cart/', include("cart.Urls"), name="cart"),
    path('header', header, name="header"),
    path('footer', footer, name="footer"),
    path('about_us', about_us, name="about_us"),
    path('contact_us', contact_us, name="contact_us"),
    
]
# command for run and make all file like static and media is "py manage.py collectstatic" but 
# you should make any folder with assets name in project
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
