# auctions/serializers.py
from rest_framework import serializers
from .models import BaseModel, Category, Item, Auction, Bid

import re

class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel


class CategorySerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Category
        fields = [
            "name",
        ]

    def validate_name(self, value):
        if not re.match(r'^[A-Za-zÀ-ÿ\s_#-]+$', value):
            raise serializers.ValidationError("Name can only contain letters, spaces and symbols (_, -, #).")
        return value


class ItemSerializer(BaseModelSerializer):
    category_name = serializers.StringRelatedField(source="category", read_only=True)

    class Meta(BaseModelSerializer.Meta):
        model = Item
        fields = [
            "name",
            "description",
            "category",
            "category_name",
            "starting_bid",
            "max_bid",
            "image",
        ]

    def validate(self, data):
        name = data.get("name", getattr(self.instance, "name", None))
        description = data.get("description", getattr(self.instance, "description", None))
        starting_bid = data.get("starting_bid", getattr(self.instance, "starting_bid", None))
        max_bid = data.get("max_bid", getattr(self.instance, "max_bid", None))

        if not re.match(r'^[A-Za-zÀ-ÿ\s-]+$', name):
            raise serializers.ValidationError("Name can only contain letters, spaces and symbols (-).")
        if not re.match(r'^[A-Za-zÀ-ÿ\s,.-]+$', description):
            raise serializers.ValidationError("Description can only contain letters, spaces and symbols (-, ,, .).")
        if max_bid:
            if max_bid <= starting_bid:
                raise serializers.ValidationError("Max bid must be greater than starting bid.")
        return data


class AuctionSerializer(BaseModelSerializer):
    item_name = serializers.StringRelatedField(source="item", read_only=True)
    owner_name = serializers.StringRelatedField(source="owner", read_only=True)
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)

    class Meta(BaseModelSerializer.Meta):
        model = Auction
        fields = [
            "name",
            "item",
            "item_name",
            "owner",
            "owner_name",
            "start_time",
            "end_time",
            "current_price",
            "status",
        ]

    def validate(self, data):
        name = data.get("name", getattr(self.instance, "name", None))
        item = data.get("item", getattr(self.instance, "item", None))
        start_time = data.get("start_time", getattr(self.instance, "start_time", None))
        end_time = data.get("end_time", getattr(self.instance, "end_time", None))
        current_price = data.get(
            "current_price", getattr(self.instance, "current_price", None)
        )

        if item:
            if current_price is None:
                current_price = item.starting_bid
                data["current_price"] = current_price
            if not (item.starting_bid <= current_price <= item.max_bid):
                raise serializers.ValidationError(
                    f"O preço atual ({current_price}) deve estar entre o lance inicial ({item.starting_bid}) "
                    f"e o lance máximo ({item.max_bid})."
                )

        if start_time >= end_time:
            raise serializers.ValidationError(
                "A hora de início deve ser anterior à hora de término."
            )

        return data

class BidSerializer(BaseModelSerializer):
    user_name = serializers.StringRelatedField(source="user", read_only=True)
    item_name = serializers.StringRelatedField(source="item", read_only=True)
    auction_name = serializers.StringRelatedField(source="auction", read_only=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)

    class Meta(BaseModelSerializer.Meta):
        model = Bid
        fields = [
            "user",
            "user_name",
            "item",
            "item_name",
            "auction",
            "auction_name",
            "amount",
        ]

    def validate(self, data):
        user = data.get("user", getattr(self.instance, "user", None))
        item = data.get("item", getattr(self.instance, "item", None))
        amount = data.get("amount", getattr(self.instance, "amount", None))

        if item:
            if amount is None:
                amount = item.starting_bid
                data["amount"] = amount
            if not (item.starting_bid <= amount <= item.max_bid):
                raise serializers.ValidationError(
                    f"O valor do lance ({amount}) deve estar entre o lance inicial ({item.starting_bid}) "
                    f"e o lance máximo ({item.max_bid})."
                )

        return data
