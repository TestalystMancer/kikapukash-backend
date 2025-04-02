from django.urls import path, include
from .views import UserCreateView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'users', UserCreateView, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
