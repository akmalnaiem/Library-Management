from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    USER_TYPES = [
        ('librarian', 'Librarian'),
        ('customer', 'Customer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    saved_books = models.JSONField(default = list)                                            # A list to store book's ID.
    cart_items = models.JSONField(default = list)

    def __str__(self):
        return f"{self.user.username}'s profile"



class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)    # Should be unique
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cover_image_url = models.URLField(blank=True, null=True)
    times_issued = models.IntegerField(default = 0)

    def __str__(self):
        return self.title    