from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer

class BaseViewSet(viewsets.ModelViewSet):
    pass

class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
