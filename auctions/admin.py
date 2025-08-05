from django.contrib import admin
from .models import Auction, Bid, Category, Item


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "item",
        "owner",
        "start_time",
        "end_time",
        "current_price",
        "status",
    )
    list_filter = ("status", "owner")
    search_fields = ("name", "item__name")


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "auction", "amount", "created_at")
    list_filter = ("auction",)
    search_fields = ("user__username", "auction__name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "starting_bid", "max_bid")
    list_filter = ("category",)
    search_fields = ("name",)
