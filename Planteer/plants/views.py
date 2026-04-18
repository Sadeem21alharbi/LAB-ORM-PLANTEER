
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Plant

# عرض كل النباتات
def all_plants_view(request: HttpRequest):
    plants = Plant.objects.all()
    return render(request, "plants/all_plants.html", {"plants": plants})

# عرض تفاصيل نبات محدد
def plant_detail_view(request: HttpRequest, plant_id: int):
    # جلب النبات بناءً على الـ ID
    plant = Plant.objects.get(id=plant_id)
    return render(request, "plants/plant_detail.html")

# إضافة نبات جديد
def add_plant_view(request: HttpRequest):
    if request.method == "POST":
        print("--- تم استلام طلب POST بنجاح ---") # هذا السطر للtest
        print(request.POST) # سيطبع لك البيانات التي كتبتيها في الـ Terminal

        new_plant = Plant(
            name=request.POST["name"],
            description=request.POST["description"],
            category=request.POST["category"],
            is_edible="is_edible" in request.POST,
            image=request.FILES.get("image") # استخدمي .get لتجنب الخطأ لو كانت فارغة
        )
        new_plant.save()
        print("--- تم حفظ النبات في قاعدة البيانات! ---")
        return redirect("plants:all_plants_view")
        
    return render(request, "plants/add_plant.html")

# تحديث بيانات نبات
def update_plant_view(request: HttpRequest, plant_id: int):
    plant = get_object_or_404(Plant, pk=plant_id)
    if request.method == "POST":
        plant.name = request.POST["name"]
        plant.description = request.POST["description"]
        plant.category = request.POST["category"]
        plant.is_edible = "is_edible" in request.POST
        if "image" in request.FILES:
            plant.image = request.FILES["image"]
        plant.save()
        return redirect("plants:plant_detail_view", plant_id=plant.id)
    return render(request, "plants/update_plant.html", {"plant": plant})

# حذف نبات
def delete_plant_view(request: HttpRequest, plant_id: int):
    plant = get_object_or_404(Plant, pk=plant_id)
    if request.method == "POST":
        plant.delete()
        return redirect("plants:all_plants_view")
    return render(request, "plants/delete_confirm.html", {"plant": plant})

# البحث عن نبات
def search_view(request: HttpRequest):
    if "search" in request.GET:
        plants = Plant.objects.filter(name__icontains=request.GET["search"])
    else:
        plants = Plant.objects.all()
    return render(request, "plants/search.html", {"plants": plants})