from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Contact

# دالة الصفحة الرئيسية
def home_view(request: HttpRequest):
    return render(request, "main/home.html")

# دالة صفحة "اتصل بنا"
def contact_view(request: HttpRequest):
    if request.method == "POST":
        # هنا سنكتب كود حفظ الرسالة لاحقاً
        pass
    return render(request, "main/contact.html")

# دالة عرض رسائل التواصل (للمدير)
def contact_messages_view(request: HttpRequest):
    # جلب كل الرسائل من قاعدة البيانات
    messages = Contact.objects.all()
    return render(request, "main/contact_messages.html", {"messages": messages})