from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('add_to_my_recipes/<int:recipe_id>/', views.add_to_my_recipes, name='add_to_my_recipes'),
    path('my_recipes/', views.my_recipes, name='my_recipes'),
    path('clear_my_recipes/', views.clear_my_recipes, name='clear_my_recipes'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
