from django.db import models
from django.contrib.auth.models import User 

class country(models.Model):
    name = models.CharField(max_length=100)
    flag = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name
    
class Plant(models.Model):
    class Category(models.TextChoices):
        TREE = 'Tree', 'Tree'
        FRUIT = 'Fruit', 'Fruit'
        VEGETABLE = 'Vegetable', 'Vegetable'
        FLOWER = 'Flower', 'Flower'

    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(
        max_length=50, 
        choices=Category.choices,
        default=Category.TREE
    )
    is_edible = models.BooleanField(default=False)
    image = models.ImageField(upload_to="images/", default="images/default.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    countries = models.ManyToManyField(country)

    def __str__(self):
        return self.name


class Comment(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.plant.name}"