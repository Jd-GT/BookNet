from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)         # título del libro
    author = models.CharField(max_length=100)        # autor
    category = models.CharField(max_length=50)       # categoría o género
    price = models.FloatField()                      # precio
    stock = models.IntegerField()                    # cantidad disponible

    def __str__(self):
        return f"{self.title} by {self.author}"
