from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(editable=False, blank=True, null=True)
    modified_at = models.DateTimeField(
        auto_now_add=False, editable=False, blank=True, null=True
    )
    is_active = models.BooleanField(default=True, editable=False)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Item(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    max_bid = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    image = models.ImageField(upload_to="auction_items/", blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Auction(BaseModel):
    name = models.CharField(max_length=100)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=[
            ("AGUARDANDO", "Aguardando"),
            ("ATIVO", "Ativo"),
            ("ENCERRADO", "Encerrado"),
            ("CANCELADO", "Cancelado"),
        ],
        default="AGUARDANDO",
    )

    class Meta:
        ordering = ["item"]

    def __str__(self):
        return self.name


class Bid(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["user"]

    def __str__(self):
        return f"{self.user} -> {self.amount} em {self.auction.item.name}"
