from django.shortcuts import render,get_list_or_404
from django.views import View
from .models import Book
class HomePageView(View):
    def get(self, request):
        return render(request, 'shop/home.html', {'title': 'Librería - Inicio'})

def book_list(request):
    books = Book.objects.all()   # consulta todos los libros de la BD
    return render(request, 'shop/book_list.html', {'books': books})

def book_detail(request, book_id):
    # Obtiene el libro por ID o muestra error 404 si no existe
    book = get_object_or_404(Book, id=book_id)
    return render(request, "shop/book_detail.html", {"book": book})