# auctions/serializers.py
from rest_framework import serializers
from .models import BaseModel, Category, Item, Auction


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        exclude_fields = [
            "created_at",
            "deleted_at",
            "modifided_at",
            "is_active",
        ]


class CategorySerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Category
        fields = [
            "name",
        ]


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


class AuctionSerializer(BaseModelSerializer):
    item_name = serializers.StringRelatedField(source="item", read_only=True)
    owner_name = serializers.StringRelatedField(source="owner", read_only=True)

    class Meta(BaseModelSerializer.Meta):
        model = Auction
        fields = [
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
        # Simula o modelo com os dados recebidos para validar as regras do clean()
        item = data.get("item", getattr(self.instance, "item", None))
        current_price = data.get(
            "current_price", getattr(self.instance, "current_price", None)
        )

        if item:
            if not (item.starting_bid <= current_price <= item.max_bid):
                raise serializers.ValidationError(
                    f"O preço atual ({current_price}) deve estar entre o lance inicial ({item.starting_bid}) "
                    f"e o lance máximo ({item.max_bid})."
                )
        return data
