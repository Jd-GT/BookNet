from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator,MaxValueValidator


class Book(models.Model):
    title = models.CharField(max_length=200)  # título del libro
    author = models.CharField(max_length=100)  # autor
    category = models.CharField(max_length=50)  # categoría o género
    price = models.FloatField()  # precio
    stock = models.IntegerField()  # cantidad disponible

    def __str__(self):
        return f"{self.title} by {self.author}"

class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # usa el modelo de usuario de Django
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    book = models.ForeignKey(
        "Book",   # referencia al modelo Book
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "book")  # un usuario no puede reseñar dos veces el mismo libro

    def __str__(self):
        return f"{self.user.username} → {self.book.title} ({self.rating}/5)"