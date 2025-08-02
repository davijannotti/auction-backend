from rest_framework import viewsets
from .models import Category, Item, Auction, Bid
from .serializers import CategorySerializer, ItemSerializer, AuctionSerializer, BidSerializer


class BaseViewSet(viewsets.ModelViewSet):
    pass


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ItemViewSet(BaseViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class AuctionViewSet(BaseViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer

class BidViewSet(BaseViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
