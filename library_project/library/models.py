from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField()
    photo = models.ImageField(upload_to='authors/', blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    cover = models.ImageField(upload_to='books/', blank=True, null=True)
    description = models.TextField()
    publication_year = models.IntegerField()
    pages = models.IntegerField()
    language = models.CharField(max_length=50)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def average_rating(self):
        reviews = self.review_set.all()
        if reviews.exists():
            return round(sum([r.rating for r in reviews]) / reviews.count(), 1)
        return 0

    def __str__(self):
        return self.title


class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(default=timezone.now)
    expected_return = models.DateField(blank=True, null=True)
    returned = models.BooleanField(default=False)
    return_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.expected_return:
            self.expected_return = timezone.now().date() + timedelta(days=14)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.book.title} - {self.rating}"