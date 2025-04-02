from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework import viewsets
from .models import CustomUser

class UserCreateView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
