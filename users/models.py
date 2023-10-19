# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from books.models import Book

class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store password hashes
    isUser = models.BooleanField(default=True)

    def __str__(self):
        return self.username

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bookId = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return self.title
