from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'image', 'rating', 'date', 'is_inspiring', 'ingredients']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control recipe-textarea', 'rows': 5}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_inspiring': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control recipe-textarea', 'rows': 5}),
        }