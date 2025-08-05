from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer
from django.utils import timezone
from rest_framework.response import Response


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to view/edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=self.request.user.pk)

    def destroy(self, request, *args, **kwargs):
        object = self.get_object()
        object.is_active = False
        object.save()
        return Response(data="delete success")
