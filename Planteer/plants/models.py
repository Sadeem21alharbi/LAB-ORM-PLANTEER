from django.db import models

class Plant(models.Model):
    # تعريف الخيارات للتصنيف (تظهر كقائمة منسدلة في لوحة التحكم)
    class Category(models.TextChoices):
        TREE = 'Tree', 'Tree'
        FRUIT = 'Fruit', 'Fruit'
        VEGETABLE = 'Vegetable', 'Vegetable'
        FLOWER = 'Flower', 'Flower'

    # الحقول الأساسية للنبات بناءً على الـ UML
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(
        max_length=50, 
        choices=Category.choices,
        default=Category.TREE
    )
    is_edible = models.BooleanField(default=False)
    
    # حقل الصورة: سيتم رفع الصور داخل مجلد media/images/
    image = models.ImageField(upload_to="images/", default="images/default.jpg")
    
    # تاريخ الإضافة (يتم تعيينه تلقائياً عند الإنشاء)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # يظهر اسم النبات في لوحة التحكم بدلاً من كلمة "Plant object"
        return self.name
