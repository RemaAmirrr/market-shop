
from django.shortcuts import render


def header(request):
    context = {
       
    }
    return render(request, "base/header.html", context)

def footer(request):
    context = {
       
    }
    return render(request, "base/footer.html", context)

def about_us(request):
    return render(request, "about_us.html", {})

def contact_us(request):
    return render(request, "contact_us.html",{})