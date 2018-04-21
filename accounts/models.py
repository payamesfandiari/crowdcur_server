from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.


class User(AbstractUser):

    email = models.EmailField("Email")
    preference = models.TextField(blank=True)
    age = models.PositiveIntegerField()
    education = models.CharField("Level of education",max_length=255)

    def __str__(self):
        return self.username


