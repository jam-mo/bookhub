from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    STATUS = (
        ('regular', 'regular'),
        ('administrator', 'adminstrator')
    )
    email = models.EmailField(unique=True, max_length=90)
    fullname = models.CharField(max_length=80)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    favourite_genres = models.CharField(max_length=150, blank=True)
    reading_history = models.CharField(max_length=300, blank=True)
    wishlist = models.CharField(max_length=300, blank=True)
    challenges = models.IntegerField(default=0)
    progress = models.IntegerField(default=0)
    status = models.CharField(max_length=60, choices=STATUS, default='regular') # d

    def __str__(self):
        return self.username

