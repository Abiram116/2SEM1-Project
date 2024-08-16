from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='recipes/')
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    is_inspiring = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Update(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
