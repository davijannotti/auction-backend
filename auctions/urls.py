# auctions/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ItemViewSet, AuctionViewSet

router = DefaultRouter()
router.register(r"categorys", CategoryViewSet)
router.register(r"itens", ItemViewSet)
router.register(r"auctions", AuctionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
