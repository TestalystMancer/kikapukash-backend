from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from savings_group.models import SavingsGroup
from .serializers import SavingsGroupSerializer, SavingsGroupMemberSerializer
from .models import SavingsGroupMember
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response


class SavingsGroupViewSet(viewsets.ModelViewSet):
    queryset = SavingsGroup.objects.all()  # Retrieve all savings groups
    serializer_class = SavingsGroupSerializer  # Use the serializer defined earlier
    permission_classes = [AllowAny]  # Ensure only authenticated users can access the viewset

    @swagger_auto_schema(
        operation_description="Retrieve a list of savings groups",
        responses={200: SavingsGroupSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        """
        List all savings groups for the authenticated user.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new savings group",
        responses={201: SavingsGroupSerializer},
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new savings group.
        The user is automatically assigned as an admin of the group.
        """
        return super().create(request, *args, **kwargs)


class SavingsGroupMemberViewSet(viewsets.ModelViewSet):
    queryset = SavingsGroupMember.objects.all()  # Retrieve all savings group members
    serializer_class = SavingsGroupMemberSerializer  # Use the serializer defined earlier
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access the viewset

    def get_queryset(self):
        """
        Optionally restricts the returned members to the current user's group.
        """
        user = self.request.user
        # Filter the members by the user's groups
        return SavingsGroupMember.objects.filter(user=user)

    @swagger_auto_schema(
        operation_description="List members of the current user's savings group",
        responses={200: SavingsGroupMemberSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        """
        List all members of the user's savings groups.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new savings group member",
        responses={201: SavingsGroupMemberSerializer},
    )
    def create(self, request, *args, **kwargs):
        """
        Add a new member to a savings group.
        This will use signals to automatically assign the user and is_admin field.
        """
        return super().create(request, *args, **kwargs)
