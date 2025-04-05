from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SavingsGroupViewSet, SavingsGroupMemberViewSet

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'groups', SavingsGroupViewSet)
router.register(r'group-members', SavingsGroupMemberViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
