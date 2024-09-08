from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.shortcuts import render
from recipes.forms import RecipeForm
from .models import Recipe, UserRecipe

#@login_required
def home(request):
    inspiring_recipes = Recipe.objects.filter(is_inspiring=True)
    for recipe in inspiring_recipes:
        recipe.ingredients_list = [ingredient.strip() for ingredient in recipe.ingredients.replace('\n', ',').split(',') if ingredient.strip()]
    
    context = {
        'inspiring_recipes': inspiring_recipes,
        'user': request.user,
    }
    return render(request, 'home.html', context)

@login_required
def profile(request):
    user_recipes = UserRecipe.objects.filter(user=request.user)
    recipes = [user_recipe.recipe for user_recipe in user_recipes]

    context = {
        'user': request.user,
        'recipes': recipes,
    }
    return render(request, 'profile.html', context)

@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.save()
            UserRecipe.objects.create(recipe=recipe, user=request.user)
            return redirect('home')
    else:
        form = RecipeForm()
    return render(request, 'create_recipe.html', {'form': form})

@login_required
def add_to_my_recipes(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    UserRecipe.objects.get_or_create(recipe=recipe, user=request.user)
    return redirect('home')

@login_required
def my_recipes(request):
    user_recipes = UserRecipe.objects.filter(user=request.user)
    recipes = [user_recipe.recipe for user_recipe in user_recipes]
    return render(request, 'my_recipes.html', {'recipes': recipes})

@login_required
def clear_my_recipes(request):
    UserRecipe.objects.filter(user=request.user).delete()
    return redirect('my_recipes')

@login_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    ingredients = [ingredient.strip() for ingredient in recipe.ingredients.replace('\n', ',').split(',') if ingredient.strip()]
    return render(request, 'recipe_detail.html', {'recipe': recipe, 'ingredients': ingredients})