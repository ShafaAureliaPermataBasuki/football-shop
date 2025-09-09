from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)              # Nama item
    price = models.IntegerField()                        # Harga item
    description = models.TextField()                     # Deskripsi item
    thumbnail = models.URLField()                        # Gambar item (URL)
    category = models.CharField(max_length=100)          # Kategori item
    is_featured = models.BooleanField(default=False)     # Status unggulan
    size = models.CharField(max_length=50, default="M")
    rating = models.FloatField(default=0)
    stock = models.IntegerField(default=0)


    def __str__(self):
        return self.name
