from typing import TYPE_CHECKING
from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

if TYPE_CHECKING:
    from auctions.models import Item
    from django.db.models.fields.related_descriptors import RelatedManager

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(
        null=False, blank=False, default=datetime.date.today()
    )
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to="users_profile_pics/", blank=True, null=True)
    items: "RelatedManager[Item]"

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "birth_date"]

    def __str__(self):
        return self.username
