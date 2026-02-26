from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Books
    path('books/', views.book_list, name='books'),
    path('book/<int:id>/', views.book_detail, name='book_detail'),

    # Borrow & Return
    path('borrow/<int:id>/', views.borrow_book, name='borrow_book'),
    path('my-books/', views.my_books, name='my_books'),
    path('return/<int:id>/', views.return_book, name='return_book'),

    # Categories
    path('categories/', views.categories_list, name='categories'),
    path('category/<int:id>/', views.category_books, name='category_books'),

    # Authors
    path('authors/', views.authors_list, name='authors'),
    path('author/<int:id>/', views.author_detail, name='author_detail'),
     # contact
    path('contact/', views.contact, name='contact'),
]