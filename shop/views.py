from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Book, Review
from .forms import ReviewForm
from django.db.models import Avg


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

    if request.method == "POST":
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.book = book
                review.user = request.user
                review.save()
                return redirect("book_detail", book_id=book.id)
        else:
            return redirect("login")
    else:
        form = ReviewForm()

    return render(request, "shop/book_detail.html", {
        "book": book,
        "reviews": reviews,
        "form": form,
        "average_rating": average_rating
    })