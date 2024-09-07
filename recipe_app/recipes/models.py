from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='recipes/')
    date = models.DateField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    is_inspiring = models.BooleanField(default=False)
    ingredients = models.TextField()

    def get_absolute_url(self):
        return reverse('recipe_detail', args=[str(self.id)])

    def __str__(self):
        return self.name

class UserRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        unique_together = ('recipe', 'user')

    def __str__(self):
        return self.recipe.name

class Update(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
