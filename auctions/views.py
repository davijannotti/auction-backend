from rest_framework import viewsets
from .models import AuctionItem
from .serializers import AuctionSerializer

class AuctionViewSet(viewsets.ModelViewSet):
    queryset = AuctionItem.objects.all()
    serializer_class = AuctionSerializer
