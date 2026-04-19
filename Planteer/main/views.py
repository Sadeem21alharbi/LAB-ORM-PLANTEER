
# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Contact
from plants.models import Plant


# دالة الصفحة الرئيسية
def home_view(request: HttpRequest):
    latest_plants = Plant.objects.all().order_by('-created_at')[:3]
    return render(request, "main/home.html", {"latest_plants": latest_plants})

def contact_view(request: HttpRequest):
    if request.method == "POST":
        new_message = Contact(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            message=request.POST["message"]
        )
        new_message.save() 
        
        return redirect("main:contact_messages_view")
    return render(request, "main/contact.html")


def contact_messages_view(request: HttpRequest):
    messages = Contact.objects.all().order_by('-created_at')
    return render(request, "main/contact_messages.html", {"messages": messages})

