import uuid
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):
    def create_superuser(self, email, password, **extra_fields):
        return super().create_superuser(email, email, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
