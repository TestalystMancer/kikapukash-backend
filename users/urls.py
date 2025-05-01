from django.urls import path, include
from .views import UserCreateView, ProfileUpdateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserCreateView, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', ProfileUpdateView.as_view(), name='user-profile-update'),
]