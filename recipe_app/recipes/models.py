from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='recipes/')
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    is_inspiring = models.BooleanField(default=False)
    ingredients = models.TextField()

    def __str__(self):
        return self.name

class Update(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message



class UserRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.recipe.name}"
