from django.conf import settings
from django.urls import include, path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('add_to_my_recipes/<int:recipe_id>/', views.add_to_my_recipes, name='add_to_my_recipes'),
    path('my_recipes/', views.my_recipes, name='my_recipes'),
    path('clear_my_recipes/', views.clear_my_recipes, name='clear_my_recipes'),
    
    # Calendar-related AJAX URLs
    path('calendar/add/', views.add_recipe_to_calendar, name='add_recipe_to_calendar'),
    path('calendar/remove/', views.remove_recipe_from_calendar, name='remove_recipe_from_calendar'),
    path('calendar/events/', views.get_user_calendar_events, name='get_user_calendar_events'),
    path('calendar/update/', views.update_event, name='update_event'),
    
    # Include Django's auth URLs
    path('accounts/', include('django.contrib.auth.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
