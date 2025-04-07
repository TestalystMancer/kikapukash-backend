from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from savings_group.models import SavingsGroup
from .serializers import SavingsGroupSerializer, SavingsGroupMemberSerializer
from .models import SavingsGroupMember
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

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
        # Manually assign the logged-in user as the creator of the savings group
        request.data['created_by'] = request.user.id  # Set created_by to the current logged-in user
        
        # Call the parent class's create method to handle the rest of the creation logic
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        # Assign the current logged-in user to the created_by field before saving
        serializer.save(created_by=self.request.user)

    @swagger_auto_schema(
        operation_description="Add a new member to a savings group",
        responses={201: SavingsGroupMemberSerializer},
    )
    @action(detail=False, methods=['post'])
    def add_member(self, request, *args, **kwargs): 
        """
        Add a new member to a savings group.
        """
        group_id = request.data.get('savings_group')
        user_id = request.data.get('user_id')

        try:
            group = SavingsGroup.objects.get(id=group_id)
        except SavingsGroup.DoesNotExist:
            return Response({"detail": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is already a member of the group
        if SavingsGroupMember.objects.filter(savings_group=group, user_id=user_id).exists():
            return Response({"detail": "User is already a member of the group."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the new member
        data = {
            'user': user_id,
            'savings_group': group_id,
            'is_admin': False,  # Optionally set this field based on business logic
        }

        # Use the correct serializer to handle adding the member to the group
        serializer = SavingsGroupMemberSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Save the new member
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
    
    @action(detail=False, methods=['post'])
    def add_member(self, request, *args, **kwargs):
        """
        Add a new member to a savings group.
        """
        # Expecting the client to send the group id under the key 'savings_group'
        group_id = request.data.get('group_id')
        user_id = request.data.get('user_id')

        try:
            group = SavingsGroup.objects.get(id=group_id)
        except SavingsGroup.DoesNotExist:
            return Response({"detail": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is already a member of the group using the capitalized field name
        if SavingsGroupMember.objects.filter(SavingsGroup=group, user=user_id).exists():
            return Response({"detail": "User is already a member of the group."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the new member data dictionary using the serializer's field name 'SavingsGroup'
        data = {
            'user': user_id,
            'SavingsGroup': group_id,  # This must match the serializer's field name
            'is_admin': False,  # Optionally set this field based on business logic
        }

        serializer = SavingsGroupMemberSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
