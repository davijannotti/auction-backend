# auctions/serializers.py
from rest_framework import serializers
from .models import Category, Item, Auction, Bid
import re

# Regex patterns for validation
NAME_REGEX = r"^[A-Za-zÀ-ÿ\s_#-]+$"
DESCRIPTION_REGEX = r"^[A-Za-zÀ-ÿ\s,.-]+$"
ITEM_NAME_REGEX = r"^[A-Za-zÀ-ÿ\s-]+$"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_name(self, value):
        if not re.match(NAME_REGEX, value):
            raise serializers.ValidationError(
                "Name can only contain letters, spaces and symbols (_, -, #)."
            )
        return value

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            "id",
            "name",
            "description",
            "category",
            "starting_bid",
            "max_bid",
            "image",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_name(self, value):
        if not re.match(ITEM_NAME_REGEX, value):
            raise serializers.ValidationError(
                "Name can only contain letters, spaces and symbols (-)."
            )
        return value

    def validate_description(self, value):
        if not re.match(DESCRIPTION_REGEX, value):
            raise serializers.ValidationError(
                "Description can only contain letters, spaces and symbols (-, ,, .)."
            )
        return value

    def validate(self, data):
        starting_bid = data.get("starting_bid", getattr(self.instance, "starting_bid", None))
        max_bid = data.get("max_bid", getattr(self.instance, "max_bid", None))

        if max_bid is not None and starting_bid is not None:
            if max_bid <= starting_bid:
                raise serializers.ValidationError(
                    "Max bid must be greater than starting bid."
                )
        return data

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = [
            "id",
            "name",
            "item",
            "owner",
            "start_time",
            "end_time",
            "current_price",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "owner", "created_at", "updated_at")

    def validate(self, data):
        item = data.get("item", getattr(self.instance, "item", None))
        start_time = data.get("start_time", getattr(self.instance, "start_time", None))
        end_time = data.get("end_time", getattr(self.instance, "end_time", None))
        current_price = data.get("current_price", getattr(self.instance, "current_price", None))

        if item:
            if current_price is None:
                current_price = item.starting_bid
                data["current_price"] = current_price

            if item.max_bid is not None and not (item.starting_bid <= current_price <= item.max_bid):
                raise serializers.ValidationError(
                    f"The current price ({current_price}) must be between the starting bid ({item.starting_bid}) "
                    f"and the max bid ({item.max_bid})."
                )
            elif item.max_bid is None and current_price < item.starting_bid:
                 raise serializers.ValidationError(
                    f"The current price ({current_price}) must be greater than or equal to the starting bid ({item.starting_bid})."
                )

        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError(
                "The start time must be before the end time."
            )

        return data

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = [
            "id",
            "user",
            "auction",
            "amount",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "user", "created_at", "updated_at")

    def validate_amount(self, value):
        auction_id = self.initial_data.get("auction")
        if not auction_id:
            if self.instance:
                auction = self.instance.auction
            else:
                return value
        else:
            try:
                auction = Auction.objects.get(pk=auction_id)
            except Auction.DoesNotExist:
                raise serializers.ValidationError("Auction does not exist.")

        if value <= auction.current_price:
            raise serializers.ValidationError(
                f"Your bid must be higher than the current price ({auction.current_price})."
            )

        if auction.item.max_bid is not None and value > auction.item.max_bid:
            raise serializers.ValidationError(
                f"Your bid cannot be higher than the maximum bid ({auction.item.max_bid})."
            )

        return value

    def validate(self, data):
        auction = data.get("auction", getattr(self.instance, "auction", None))
        user = self.context['request'].user

        if auction and user and auction.owner == user:
            raise serializers.ValidationError("You cannot bid on your own auction.")

        return data
