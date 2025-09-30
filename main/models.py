from django.db import models
from django.contrib.auth.models import User
import uuid

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)              # Nama item
    price = models.IntegerField()                        # Harga item
    description = models.TextField()                     # Deskripsi item
    thumbnail = models.URLField()                        # Gambar item (URL)
    category = models.CharField(max_length=100)          # Kategori item
    is_featured = models.BooleanField(default=False)     # Status unggulan
    size = models.CharField(max_length=50, default="M")
    rating = models.FloatField(default=0)
    stock = models.IntegerField(default=0)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

