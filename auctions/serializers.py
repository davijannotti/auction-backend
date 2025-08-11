from rest_framework import serializers
from users.models import User
from .models import BaseModel, Category, Item, Auction, Bid
import re

# Regex patterns for validation
NAME_REGEX = r"^[A-Za-zÀ-ÿ\s_#-]+$"
DESCRIPTION_REGEX = re.compile(
    r"^[\w\s.,\-:;!?()'\"%&@#/$\[\]{}<>°ºªÀ-ÖØ-öø-ÿ]+$", re.UNICODE
)
ITEM_NAME_REGEX = r"^[A-Za-zÀ-ÿ\s-]+$"


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        fields = [
            "id",
            "created_at",
            "deleted_at",
            "updated_at",
            "is_active",
        ]


class UserStatisticsSerializer(BaseModelSerializer):
    instance: User|None
    acquired_items = serializers.SerializerMethodField()
    auctions_participated = serializers.SerializerMethodField()

    class Meta(BaseModelSerializer.Meta):
        model = User
        fields = [
            "acquired_items",
            "auctions_participated",
        ]

    @property
    def items(self):
        assert self.instance is not None
        return self.instance.items

    def get_acquired_items(self, instance):
        return ItemSerializer(self.items, many=True).data

    def get_auctions_participated(self, instance):
        auctions = Auction.objects.filter(items__bid__user=instance).distinct()
        return AuctionSerializer(auctions, many=True).data

class CategorySerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Category
        fields = BaseModelSerializer.Meta.fields + ["name"]

    def validate_name(self, value):
        if not re.match(NAME_REGEX, value):
            raise serializers.ValidationError(
                "Name can only contain letters, spaces, and symbols (_, -, #)."
            )
        return value


class ItemSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Item
        fields = BaseModelSerializer.Meta.fields + [
            "name",
            "description",
            "starting_bid",
            "max_bid",
            "current_bid",
            "auction",
            "image",
        ]
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_name(self, value):
        if not re.match(ITEM_NAME_REGEX, value):
            raise serializers.ValidationError(
                "Name can only contain letters, spaces, and hyphens (-)."
            )
        return value

    def validate_description(self, value):
        if not re.match(DESCRIPTION_REGEX, value):
            raise serializers.ValidationError(
                "Description can only contain letters, spaces, and symbols (-, ,, .)."
            )
        return value

    def validate(self, data):
        data = super().validate(data)

        starting_bid = data.get(
            "starting_bid", getattr(self.instance, "starting_bid", None)
        )
        max_bid = data.get("max_bid", getattr(self.instance, "max_bid", None))

        if max_bid is not None and starting_bid is not None:
            if max_bid <= starting_bid:
                raise serializers.ValidationError(
                    "Max bid must be greater than starting bid."
                )
        return data


class AuctionSerializer(BaseModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta(BaseModelSerializer.Meta):
        model = Auction
        fields = BaseModelSerializer.Meta.fields + [
            "name",
            "category",
            "owner",
            "start_time",
            "end_time",
            "status",
            "items",
        ]
        read_only_fields = BaseModelSerializer.Meta.fields + ["owner"]

    def get_items(self, obj):
        """Retorna todos os itens deste leilão usando a função get_items() do modelo"""
        items = obj.get_items()
        return ItemSerializer(items, many=True).data

    def validate(self, data):
        data = super().validate(data)

        start_time = data.get("start_time", getattr(self.instance, "start_time", None))
        end_time = data.get("end_time", getattr(self.instance, "end_time", None))

        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError(
                "The start time must be before the end time."
            )

        return data


class BidSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Bid
        fields = BaseModelSerializer.Meta.fields + [
            "user",
            "item",
            "amount",
        ]
        read_only_fields = BaseModelSerializer.Meta.fields + ["user"]

    def validate_amount(self, value):
        item_id = self.initial_data.get("item")
        if not item_id and self.instance:
            item_id = self.instance.item.id

        if not item_id:
            raise serializers.ValidationError("Item must be provided for the bid.")

        try:
            item_instance = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            raise serializers.ValidationError("Item does not exist.")

        # Assuming 'current_bid' and 'max_bid' are fields on the Item model
        if value <= item_instance.current_bid:
            raise serializers.ValidationError(
                f"Your bid must be higher than the current bid ({item_instance.current_bid})."
            )

        if item_instance.max_bid is not None and value > item_instance.max_bid:
            raise serializers.ValidationError(
                f"Your bid cannot be higher than the maximum bid ({item_instance.max_bid})."
            )

        return value

    def validate(self, data):
        data = super().validate(data)
        user = self.context["request"].user
        item = data.get("item", getattr(self.instance, "item", None))

        if item:
            auction = item.auction
            if auction and user and auction.owner == user:
                raise serializers.ValidationError("You cannot bid on your own auction.")
        else:
            raise serializers.ValidationError("Item must be provided for the bid.")

        return data
