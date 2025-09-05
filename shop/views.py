from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Book, Review, Cart, CartItem
from .forms import ReviewForm
from django.db.models import Avg
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages


class HomePageView(View):
    def get(self, request):
        return render(request, "shop/home.html", {"title": "Librería - Inicio"})


def book_list(request):
    books = Book.objects.all()  # consulta todos los libros de la BD
    return render(request, "shop/book_list.html", {"books": books})


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all()

    # calcular promedio de rating
    average_rating = reviews.aggregate(Avg("rating"))["rating__avg"]

    message = None
    if request.method == "POST":
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.book = book
                review.user = request.user
                try:
                    review.save()
                    return redirect("book_detail", book_id=book.id)
                except Exception as e:
                    # Si el usuario ya reseñó el libro
                    from django.db import IntegrityError
                    if isinstance(e, IntegrityError):
                        message = "No puedes volver a reseñar este libro porque ya lo has hecho."
                    else:
                        message = "Ocurrió un error al guardar la reseña."
        else:
            return redirect("login")
    else:
        form = ReviewForm()

    return render(request, "shop/book_detail.html", {
        "book": book,
        "reviews": reviews,
        "form": form,
        "average_rating": average_rating,
        "message": message
    })

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # loguear automáticamente
            return redirect("book_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if book.stock < 1:
        return render(request, "shop/out_of_stock.html", {"book": book})

    cart = Cart.objects.get(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect("view_cart")


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    total = sum(item.book.price * item.quantity for item in cart.items.all())
    return render(request, "shop/cart.html", {"cart": cart, "total": total})


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect("view_cart")

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    for item in cart.items.all():
        if item.book.stock >= item.quantity:
            item.book.stock -= item.quantity
            item.book.save()
        else:
            return render(request, "shop/out_of_stock.html", {"book": item.book})
    cart.items.all().delete()
    return render(request, "shop/checkout_success.html")

def update_quantity(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if action == "increase":
        if item.quantity < item.book.stock:
            item.quantity += 1
            item.save()
        else:
            messages.error(request, "No more stock available for this book.")
    elif action == "decrease":
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()  # si llega a 0, se elimina
    return redirect("view_cart")