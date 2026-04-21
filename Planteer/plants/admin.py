from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Plant, Comment, country

admin.site.register(Plant)
admin.site.register(Comment)
admin.site.register(country)
