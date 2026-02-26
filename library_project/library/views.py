from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.core.mail import send_mail

from .models import Book, Borrow, Category, Author, Review

def home(request):
    return render(request, 'home.html')


def book_list(request):
    books = Book.objects.all()

    search_query = request.GET.get('search')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__name__icontains=search_query)
        )

    sort = request.GET.get('sort')
    if sort == 'newest':
        books = books.order_by('-created_at')
    elif sort == 'oldest':
        books = books.order_by('created_at')

    paginator = Paginator(books, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'books.html', {'page_obj': page_obj})


def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'book_detail.html', {'book': book})

@login_required
def borrow_book(request, id):
    book = get_object_or_404(Book, id=id)

    if book.available_copies <= 0:
        messages.error(request, "No copies available.")
        return redirect('book_detail', id=id)

    if Borrow.objects.filter(user=request.user, book=book, returned=False).exists():
        messages.warning(request, "You already borrowed this book.")
        return redirect('book_detail', id=id)

    if Borrow.objects.filter(user=request.user, returned=False).count() >= 5:
        messages.error(request, "Maximum 5 books allowed.")
        return redirect('book_detail', id=id)

    Borrow.objects.create(
        user=request.user,
        book=book,
        borrow_date=timezone.now().date(),
        expected_return=timezone.now().date() + timedelta(days=14),
        returned=False
    )

    # تحديث آمن مباشر من قاعدة البيانات
    Book.objects.filter(id=book.id, available_copies__gt=0).update(
        available_copies=F('available_copies') - 1
    )

    messages.success(request, "Book borrowed successfully!")
    return redirect('book_detail', id=id)

@login_required
def my_books(request):
    borrows = Borrow.objects.filter(
        user=request.user,
        returned=False
    )
    return render(request, 'my_books.html', {'borrows': borrows})

@login_required
def return_book(request, id):
    borrow = get_object_or_404(
        Borrow,
        id=id,
        user=request.user,
        returned=False
    )

    borrow.returned = True
    borrow.save()

    book = borrow.book

    # لا نسمح بتجاوز العدد الكلي
    if book.available_copies < book.total_copies:
        Book.objects.filter(id=book.id).update(
            available_copies=F('available_copies') + 1
        )

    messages.success(request, "Book returned successfully!")
    return redirect('my_books')


# ==========================
# Categories
# ==========================

def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})


def category_books(request, id):
    category = get_object_or_404(Category, id=id)
    books = Book.objects.filter(category=category)
    return render(request, 'category_books.html', {
        'category': category,
        'books': books
    })


# ==========================
# Authors
# ==========================

def authors_list(request):
    authors = Author.objects.all()
    return render(request, 'authors.html', {'authors': authors})


def author_detail(request, id):
    author = get_object_or_404(Author, id=id)
    books = Book.objects.filter(author=author)
    return render(request, 'author_detail.html', {
        'author': author,
        'books': books
    })



def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')

    return render(request, 'contact.html')