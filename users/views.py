from auctions.serializers import UserStatisticsSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.decorators import action
from rest_framework.request import Request
from django.db.models import Count

from rest_framework.authentication import SessionAuthentication
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer

from rest_framework.authentication import BaseAuthentication


class NoAuth(BaseAuthentication):
    """
    Autenticação "vazia" para permitir acesso sem exigir CSRF ou token.
    """

    def authenticate(self, request):
        return None


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to view/edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Instance-level permission to only allow owner of an object or admin to edit it.
        return obj == request.user or request.user.is_staff


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    @action(detail=True, methods=["GET"])
    def statistics(self, request: Request, pk=id):
        user = self.get_object()
        data = UserStatisticsSerializer(instance=user).data
        return Response(data)

    @action(detail=False, methods=["GET"])
    def ranking(self, request):
        ranking = User.objects.annotate(items_count=Count("items")).order_by("-items_count")
        serializer = UserSerializer(ranking, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        """
        Admins can see all users.
        Regular users can only see their own profile.
        """
        if self.request.user.is_staff:
            return User.objects.all().order_by("-date_joined")
        return User.objects.filter(pk=self.request.user.pk)

    def destroy(self, request, *args, **kwargs):
        """
        Instead of deleting, this performs a "soft delete" by deactivating the user.
        """
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(
            data={"message": "User deactivated successfully."},
            status=status.HTTP_200_OK,
        )


class UserRegistrationView(CreateAPIView):
    """
    Public API view for creating (registering) a new user.
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]  # Libera para todos
    authentication_classes = [NoAuth]  # Remove autenticação/CSRF

    def create(self, request, *args, **kwargs):
        """
        Overrides the default create method to return a custom success message.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        response_data = {
            "message": "User registered successfully.",
            "user_id": serializer.instance.id,
            "username": serializer.instance.username,
            "email": serializer.instance.email,
        }

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
