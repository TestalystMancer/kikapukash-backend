from django.urls import path, include
from rest_framework.routers import DefaultRouter
from savings_group.views import SavingsGroupViewSet, SavingsGroupMemberViewSet

router = DefaultRouter()
router.register(r'groups', SavingsGroupViewSet, basename='savingsgroup')
router.register(r'group-members', SavingsGroupMemberViewSet, basename='savingsgroupmember')  # ✅ basename added

urlpatterns = [
    path('', include(router.urls)),
]
