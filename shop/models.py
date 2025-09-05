from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User


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
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.book.title} x {self.quantity}"

    def subtotal(self):
        return self.book.price * self.quantity