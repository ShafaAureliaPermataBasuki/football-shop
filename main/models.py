import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    CATEGORY_CHOICES = [
        ('shoes', 'Shoes'),
        ('clothes', 'Clothes'),
        ('equipment', 'Equipment'),
        ('accessories', 'Accessories'),
        ('misc', 'Miscellaneous'),
    ]
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    rating = models.FloatField(default=0.0, validators=[MaxValueValidator(5.0), MinValueValidator(0.0)])
    views = models.IntegerField(default=0) 
    thumbnail = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='shoes')
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    @property
    def is_hot(self):
        return self.views > 20

    def increment_views(self):
        self.views += 1
        self.save()