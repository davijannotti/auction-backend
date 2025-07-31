# auctions/serializers.py
from rest_framework import serializers
from .models import AuctionItem, BaseModel

class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        fields = [
            "created_at",
            "deleted_at",
            "modifided_at",
            "is_active",
        ]


class AuctionSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = AuctionItem
        fields = [
            "title",
            "description",
            "starting_bid",
            "max_bid",
        ]
