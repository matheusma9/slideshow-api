from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .permission import IsOwnerOrCreateOnly


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all() 
    permission_classes = [IsOwnerOrCreateOnly]

    

