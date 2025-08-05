from django.contrib import admin
from django import forms
from .models import Auction, Bid, Category, Item
import re
from django.core.exceptions import ValidationError

# Regex patterns
NAME_REGEX = r"^[A-Za-zÀ-ÿ\s_#-]+$"
DESCRIPTION_REGEX = r"^[A-Za-zÀ-ÿ\s,.-]+$"
ITEM_NAME_REGEX = r"^[A-Za-zÀ-ÿ\s-]+$"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not re.match(NAME_REGEX, name):
            raise ValidationError(
                "Name can only contain letters, spaces, and symbols (_, -, #)."
            )
        return name


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not re.match(ITEM_NAME_REGEX, name):
            raise ValidationError(
                "Name can only contain letters, spaces, and hyphens (-)."
            )
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if not re.match(DESCRIPTION_REGEX, description):
            raise ValidationError(
                "Description can only contain letters, spaces, and symbols (-, ,, .)."
            )
        return description

    def clean(self):
        cleaned_data = super().clean()
        starting_bid = cleaned_data.get("starting_bid")
        max_bid = cleaned_data.get("max_bid")

        if max_bid is not None and starting_bid is not None:
            if max_bid <= starting_bid:
                raise ValidationError("Max bid must be greater than starting bid.")
        return cleaned_data


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get("item")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        current_price = cleaned_data.get("current_price")

        if item:
            if current_price is None:
                current_price = item.starting_bid
                cleaned_data["current_price"] = current_price

            if item.max_bid is not None:
                if not (item.starting_bid <= current_price <= item.max_bid):
                    raise ValidationError(
                        f"The current price ({current_price}) must be between the starting bid ({item.starting_bid}) "
                        f"and the max bid ({item.max_bid})."
                    )
            elif current_price < item.starting_bid:
                raise ValidationError(
                    f"The current price ({current_price}) must be greater than or equal to the starting bid ({item.starting_bid})."
                )

        if start_time and end_time and start_time >= end_time:
            raise ValidationError("The start time must be before the end time.")
        return cleaned_data


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = "__all__"

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        auction = self.cleaned_data.get("auction")

        if auction:
            if amount <= auction.current_price:
                raise ValidationError(
                    f"Your bid must be higher than the current price ({auction.current_price})."
                )

            if auction.item.max_bid is not None and amount > auction.item.max_bid:
                raise ValidationError(
                    f"Your bid cannot be higher than the maximum bid ({auction.item.max_bid})."
                )
        return amount

    def clean(self):
        cleaned_data = super().clean()
        auction = cleaned_data.get("auction")
        user = cleaned_data.get("user")

        if auction and user and auction.owner == user:
            raise ValidationError("You cannot bid on your own auction.")
        return cleaned_data


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    form = AuctionForm
    list_display = (
        "name",
        "owner",
        "start_time",
        "end_time",
        "status",
    )
    list_filter = ("status", "owner")
    search_fields = ("name",)


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    form = BidForm
    list_display = ("user", "amount", "created_at")
    search_fields = ("user__username",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    form = ItemForm
    list_display = ("name", "starting_bid", "max_bid")
    search_fields = ("name",)
