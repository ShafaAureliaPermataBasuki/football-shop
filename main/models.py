from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import uuid

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # sementara nullable
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    size = models.CharField(max_length=50, default="M")
    rating = models.FloatField(default=0)
    stock = models.IntegerField(default=0)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True) # kasih default supaya migration aman

    def __str__(self):
        return self.name
