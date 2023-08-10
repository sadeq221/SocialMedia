from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username