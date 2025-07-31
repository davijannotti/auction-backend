from xmlrpc.client import MAXINT
from django.db import models

class AuctionItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    max_bid = models.DecimalField(max_digits=10, decimal_places=2, default=MAXINT)

    def __str__(self):
        return self.title
