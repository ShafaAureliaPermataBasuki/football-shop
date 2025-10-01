from django.forms import ModelForm
from main.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["brand", "name", "description", "price", "rating", "thumbnail", "category", "is_featured"]