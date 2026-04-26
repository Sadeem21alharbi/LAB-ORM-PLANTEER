from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .models import Plant, Comment, country
from django.contrib import messages 
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse

# دالة التحقق من الأدمن
def is_admin(user):
    return user.is_superuser

# --- 1. عرض كل النباتات ---
def all_plants_view(request: HttpRequest):
    plants = Plant.objects.all()
    countries = country.objects.all() 
    
    category = request.GET.get("category")
    is_edible = request.GET.get("is_edible")
    country_id = request.GET.get("country") 

    if category and category != "":
        plants = plants.filter(category__icontains=category.strip())
    
    if is_edible and is_edible != "":
        plants = plants.filter(is_edible=(is_edible == "True"))

    if country_id and country_id != "":
        plants = plants.filter(countries__id=country_id)

    return render(request, "plants/all_plants.html", {
        "plants": plants, 
        "countries": countries
    })

# --- 2. تفاصيل النبات والتعليقات ---
def plant_detail_view(request: HttpRequest, plant_id: int):
    plant = get_object_or_404(Plant, pk=plant_id)
   
    if request.method == "POST":
        if request.user.is_authenticated:
            new_comment = Comment(
                plant=plant, 
                user=request.user,
                content=request.POST["content"]
            )
            new_comment.save()
            messages.success(request, "تم إضافة تعليقك بنجاح!") 
            # العودة لنفس النقطة باستخدام Anchor
            return redirect(reverse("plants:plant_detail_view", kwargs={"plant_id": plant.id}) + "#comments-section")
        else:
            messages.error(request, "لا تستطيع كتابة تعليق بدون تسجيل دخول.")
            return redirect(reverse("plants:plant_detail_view", kwargs={"plant_id": plant.id}) + "#comments-section")

    comments = Comment.objects.filter(plant=plant).order_by('-created_at')
    related_plants = Plant.objects.filter(category=plant.category, is_edible=plant.is_edible).exclude(id=plant.id)[:3]

    return render(request, "plants/plant_detail.html", {
        "plant": plant,
        "related_plants": related_plants,
        "comments": comments
    })

# --- 3. إضافة نبات (للأدمن فقط) ---
@user_passes_test(is_admin, login_url="accounts:login_view")
def add_plant_view(request: HttpRequest):
    if request.method == "POST":
        new_plant = Plant(
            name=request.POST["name"],
            description=request.POST["description"],
            category=request.POST["category"],
            is_edible="is_edible" in request.POST,
            image=request.FILES.get("image")
        )
        new_plant.save()
        return redirect("plants:all_plants_view")
        
    return render(request, "plants/add_plant.html")

# --- 4. تحديث نبات (للأدمن فقط) ---
@user_passes_test(is_admin, login_url="accounts:login_view")
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

# --- 5. حذف نبات (للأدمن فقط) ---
@user_passes_test(is_admin, login_url="accounts:login_view")
def delete_plant_view(request: HttpRequest, plant_id: int):
    plant = get_object_or_404(Plant, pk=plant_id)
    plant.delete()  
    return redirect("plants:all_plants_view")

# --- 6. البحث ---
def search_view(request: HttpRequest):
    query = request.GET.get("search") or request.GET.get("search_input") or ""
    if query:
        plants = Plant.objects.filter(name__icontains=query) | Plant.objects.filter(description__icontains=query)
    else:
        plants = Plant.objects.none()
    return render(request, "plants/search.html", {"plants": plants, "query": query})