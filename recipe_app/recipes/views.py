from django.shortcuts import render, get_object_or_404
from .models import Recipe

def home(request):
    # Fetch inspiring recipes - adjust query as needed
    inspiring_recipes = Recipe.objects.all()[:6]  # Example: get the first 6 recipes
    context = {
        'inspiring_recipes': inspiring_recipes,
    }
    return render(request, 'home.html', context)

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    context = {
        'recipe': recipe,
    }
    return render(request, 'recipe_detail.html', context)
