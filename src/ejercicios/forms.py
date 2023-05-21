from django import forms
from .models import ProductModels

class ProductModelsForm(forms.ModelForm):
    class Meta:
        model = ProductModels
        fields = [
            "title",
            "price",
            "description",
            "color",
        ]