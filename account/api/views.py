from rest_framework import viewsets
from ..models import User
from .serializers import UserSerializer
from .permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
