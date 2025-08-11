from typing import TYPE_CHECKING
from django.db import models
from django.conf import settings
from enum import Enum

if TYPE_CHECKING:
    from django.db.models.fields.related_descriptors import RelatedManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return str(self.name)


class Item(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    starting_bid = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )
    max_bid = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    current_bid = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    image = models.ImageField(upload_to="auction_items/", blank=True, null=True)
    auction = models.ForeignKey(
        "Auction",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="items",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="items",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return str(self.name)


class Auction(BaseModel):
    class Status(Enum):
        AGUARDANDO = "Aguardando"
        ATIVO = "Ativo"
        ENCERRADO = "Encerrado"
        CANCELADO = "Cancelado"

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=False, blank=False)
    status = models.CharField(
        max_length=20,
        choices=[(status.name, status.value) for status in Status],
        default=Status.AGUARDANDO.name,
    )
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    items: "RelatedManager[Item]"

    class Meta:
        ordering = ["name"]

    def get_items(self):
        """Retorna todos os itens deste leilão"""
        return self.items.all()

    def __str__(self):
        return str(self.name)


class Bid(BaseModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )

    class Meta:
        ordering = ["item"]

    def __str__(self):
        return f"{self.user} -> ${self.amount} em {self.item.name}"
