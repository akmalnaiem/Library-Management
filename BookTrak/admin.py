from django.contrib import admin
from .models import UserProfile, Book

admin.site.register(UserProfile)

# Registering Book model--
admin.site.register(Book)