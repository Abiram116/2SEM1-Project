from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import CalendarEvent, Recipe, UserRecipe, UserProfile
from .forms import UserProfileForm
from django.views.decorators.csrf import csrf_exempt

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Ensure a UserProfile is created for the new user
            UserProfile.objects.get_or_create(user=user)
            return redirect('calendar_view')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('calendar_view')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')  # Redirect to home after logout

@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'user_profile.html', {'form': form})

def home(request):
    inspiring_recipes = Recipe.objects.all()[:6]
    for recipe in inspiring_recipes:
        recipe.ingredients_list = [ingredient.strip() for ingredient in recipe.ingredients.split(',')]
    context = {
        'inspiring_recipes': inspiring_recipes,
    }
    return render(request, 'home.html', context)

@csrf_exempt
@login_required
def add_recipe_to_calendar(request):
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        start_time = request.POST.get('start_time')
        try:
            recipe = Recipe.objects.get(id=recipe_id)
            user = request.user
            CalendarEvent.objects.update_or_create(
                user=user,
                recipe=recipe,
                defaults={'start_time': start_time}
            )
            return JsonResponse({'status': 'success'})
        except Recipe.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Recipe not found'}, status=404)
    return JsonResponse({'status': 'fail'}, status=400)

@login_required
def get_user_calendar_events(request):
    user = request.user
    events = CalendarEvent.objects.filter(user=user).values('id', 'recipe__name', 'start_time')
    event_list = []
    for event in events:
        event_list.append({
            'id': event['id'],
            'title': event['recipe__name'],
            'start': event['start_time'].isoformat(),
            'allDay': True,
        })
    return JsonResponse({'events': event_list})

@csrf_exempt
@login_required
def remove_recipe_from_calendar(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        if CalendarEvent.objects.filter(id=event_id, user=request.user).exists():
            CalendarEvent.objects.filter(id=event_id, user=request.user).delete()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'fail', 'message': 'Event not found'}, status=404)
    return JsonResponse({'status': 'fail'}, status=400)

@csrf_exempt
@login_required
def update_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        start_time = request.POST.get('start_time')
        try:
            event = CalendarEvent.objects.get(id=event_id, user=request.user)
            event.start_time = start_time
            event.save()
            return JsonResponse({'status': 'success'})
        except CalendarEvent.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Event not found'}, status=404)
    return JsonResponse({'status': 'fail'}, status=400)

@login_required
def add_to_my_recipes(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user_recipe, created = UserRecipe.objects.get_or_create(user=request.user, recipe=recipe)
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
def calendar_view(request):
    user_recipes = UserRecipe.objects.filter(user=request.user)
    recipes = [user_recipe.recipe for user_recipe in user_recipes]
    return render(request, 'calendar.html', {'recipes': recipes})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    ingredients = [ingredient.strip() for ingredient in recipe.ingredients.split(',')]
    return render(request, 'recipe_detail.html', {'recipe': recipe, 'ingredients': ingredients})
