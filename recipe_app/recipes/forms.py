from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'image', 'rating','date', 'is_inspiring','ingredients']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'ingredients': forms.Textarea(attrs={'rows': 5}),
        }