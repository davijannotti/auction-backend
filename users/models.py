from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # O campo 'username' é fornecido por AbstractUser, não precisa ser redeclarado aqui.
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to="users_profile_pics/", blank=True, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "birth_date"]

    def __str__(self):
        return self.username
