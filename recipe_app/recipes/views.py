from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe

def home(request):
    inspiring_recipes = Recipe.objects.all()[:6]
    for recipe in inspiring_recipes:
        recipe.ingredients_list = recipe.ingredients.split(',')
    context = {
        'inspiring_recipes': inspiring_recipes,
    }
    return render(request, 'home.html', context)


def add_to_my_recipes(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    my_recipes = request.session.get('my_recipes', [])
    
    if recipe_id not in my_recipes:
        my_recipes.append(recipe_id)
        # save it back to the session
    request.session['my_recipes'] = my_recipes
    return redirect('home')


def my_recipes(request):
    # get the recipe IDs stored in the session
    recipe_ids = request.session.get('my_recipes', [])
    
    # Retrieve the actual Recipe objects from the database
    recipes = Recipe.objects.filter(id__in=recipe_ids)
    
    return render(request, 'my_recipes.html', {'recipes': recipes})

def clear_my_recipes(request):
    # Clear the session data for "my_recipes"
    request.session['my_recipes'].clear()
    return redirect('my_recipes')

def recipe_detail(request, pk):
    # Retrieve the recipe by primary key (pk)
    recipe = get_object_or_404(Recipe, pk=pk)
    ingredients = [ingredient.strip() for ingredient in recipe.ingredients.split(',')]
    return render(request, 'recipe_detail.html', {'recipe': recipe, 'ingredients': ingredients})