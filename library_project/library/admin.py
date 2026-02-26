from django.contrib import admin
from .models import Author, Category, Book, Borrow, Review


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 10


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'total_copies', 'available_copies', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'author__name')
    list_per_page = 10
    ordering = ('-created_at',)


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'expected_return', 'returned')
    list_filter = ('returned', 'borrow_date')
    search_fields = ('user__username', 'book__title')
    list_per_page = 10


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('book__title', 'user__username')
    list_per_page = 10