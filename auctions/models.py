from xmlrpc.client import MAXINT
from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(editable=False, blank=True, null=True)
    modifided_at = models.DateTimeField(auto_now_add=False, editable=False, blank=True, null=True)
    is_active = models.BooleanField(default=True, editable=False)

class AuctionItem(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    max_bid = models.DecimalField(max_digits=10, decimal_places=2, default=MAXINT)

    def __str__(self):
        return self.title
