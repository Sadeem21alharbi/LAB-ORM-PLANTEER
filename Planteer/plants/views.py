
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Plant, Comment, country

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

def plant_detail_view(request: HttpRequest, plant_id: int):
    plant = get_object_or_404(Plant, pk=plant_id)
   
    if request.method == "POST":
        new_comment = Comment(
            plant=plant, 
            name=request.POST["name"], 
            content=request.POST["content"]
        )
        new_comment.save()
        return redirect("plants:plant_detail_view", plant_id=plant.id)

    comments = Comment.objects.filter(plant=plant).order_by('-created_at')

    related_plants = Plant.objects.filter(
        category=plant.category, 
        is_edible=plant.is_edible
    ).exclude(id=plant.id)[:3]

    return render(request, "plants/plant_detail.html", {
        "plant": plant,
        "related_plants": related_plants,
        "comments": comments
    })

def add_plant_view(request: HttpRequest):
    if request.method == "POST":
        print("--- تم استلام طلب POST بنجاح ---") 
        print(request.POST) 

        new_plant = Plant(
            name=request.POST["name"],
            description=request.POST["description"],
            category=request.POST["category"],
            is_edible="is_edible" in request.POST,
            image=request.FILES.get("image")
        )
        new_plant.save()
        print("--- تم حفظ النبات في قاعدة البيانات! ---")
        return redirect("plants:all_plants_view")
        
    return render(request, "plants/add_plant.html")

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

def delete_plant_view(request: HttpRequest, plant_id: int):
    plant = get_object_or_404(Plant, pk=plant_id)
    plant.delete()  
    return redirect("plants:all_plants_view")

def search_view(request: HttpRequest):
    query = request.GET.get("search") or request.GET.get("search_input") or ""
    
    if query:
        plants = Plant.objects.filter(name__icontains=query) | Plant.objects.filter(description__icontains=query)
    else:
        plants = Plant.objects.none()

    return render(request, "plants/search.html", {"plants": plants, "query": query})