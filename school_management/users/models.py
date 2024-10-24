from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Office Staff'),
        ('librarian', 'Librarian'),
        ('student', 'Student'),
    )
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
    )

    role = models.CharField(max_length=15, choices=ROLE_CHOICES)
    mob = models.CharField(max_length=10, blank=True)
    profile_pic = models.ImageField(upload_to='Profile Picture')  
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1 , choices=GENDER_CHOICES)
    def __str__(self):
        return self.name
