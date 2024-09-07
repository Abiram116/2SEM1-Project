from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Commented out calendar-related URL patterns
    # path('calendar/', views.calendar_view, name='calendar_view'),
    # path('calendar/add/', views.add_recipe_to_calendar, name='add_recipe_to_calendar'),
    # path('calendar/remove/', views.remove_recipe_from_calendar, name='remove_recipe_from_calendar'),
    # path('calendar/events/', views.get_user_calendar_events, name='get_user_calendar_events'),
    # path('calendar/update/', views.update_event, name='update_event'),

    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('add_to_my_recipes/<int:recipe_id>/', views.add_to_my_recipes, name='add_to_my_recipes'),
    path('my_recipes/', views.my_recipes, name='my_recipes'),
    path('clear_my_recipes/', views.clear_my_recipes, name='clear_my_recipes'),
    path('create/', views.create_recipe, name='create_recipe'),  # Ensure there's only one entry for create_recipe

    # Authentication-related URLs
    path('accounts/', include('allauth.urls')),

    # Add the profile URL pattern
    path('profile/', views.profile, name='profile'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
