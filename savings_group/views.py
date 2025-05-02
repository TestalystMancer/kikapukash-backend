# from rest_framework import viewsets, status
# from rest_framework.permissions import IsAuthenticated  # Removed AllowAny for safety
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework.exceptions import ValidationError

# from savings_group.models import SavingsGroup, SavingsGroupMember
# from .serializers import SavingsGroupSerializer, SavingsGroupMemberSerializer

# class SavingsGroupViewSet(viewsets.ModelViewSet):
#     queryset = SavingsGroup.objects.all()  # Retrieve all savings groups
#     serializer_class = SavingsGroupSerializer  # Use the serializer defined earlier
#     permission_classes = [IsAuthenticated]  # Now only authenticated users can access

#     @swagger_auto_schema(
#         operation_description="Retrieve a list of savings groups",
#         responses={200: SavingsGroupSerializer(many=True)},
#     )
#     def list(self, request, *args, **kwargs):
#         """
#         List all savings groups.
#         """
#         return super().list(request, *args, **kwargs)

#     @swagger_auto_schema(
#         operation_description="Create a new savings group",
#         responses={201: SavingsGroupSerializer},
#     )
#     def create(self, request, *args, **kwargs):
#         """
#         Create a new savings group.
#         The user is automatically assigned as the admin (creator) of the group.
#         """
#         request.data['created_by'] = request.user.id
#         return super().create(request, *args, **kwargs)
    
#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user)

#     # Removed add_member from this viewset to avoid duplication


# class SavingsGroupMemberViewSet(viewsets.ModelViewSet):
#     serializer_class = SavingsGroupMemberSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         """
#         Return members for all groups the current user belongs to.
#         """
#         user = self.request.user
#         # Get IDs of groups the user is a member of
#         user_groups = SavingsGroupMember.objects.filter(user=user).values_list('savings_group_id', flat=True)
#         return SavingsGroupMember.objects.filter(savings_group_id__in=user_groups)

#     @swagger_auto_schema(
#         operation_description="List members of the user's savings groups",
#         responses={200: SavingsGroupMemberSerializer(many=True)},
#     )
#     def list(self, request, *args, **kwargs):
#         """
#         List all members of groups the user belongs to.
#         """
#         return super().list(request, *args, **kwargs)

#     @swagger_auto_schema(
#         operation_description="Create a new savings group member",
#         responses={201: SavingsGroupMemberSerializer},
#     )
#     def create(self, request, *args, **kwargs):
#         """
#         Add a new member to a savings group.
#         """
#         return super().create(request, *args, **kwargs)
    
#     @swagger_auto_schema(
#         method='post',
#         operation_description="Add a new member to a savings group",
#         responses={201: SavingsGroupMemberSerializer},
#     )
#     @action(detail=False, methods=['post'])
#     def add_member(self, request, *args, **kwargs):
#         """
#         Add a new member to a savings group.
#         Expected JSON body:
#         {
#             "savings_group": <group_id>,
#             "user_id": <user_id>
#         }
#         """
#         group_id = request.data.get('savings_group')
#         user_id = request.data.get('user_id')

#         try:
#             group = SavingsGroup.objects.get(id=group_id)
#         except SavingsGroup.DoesNotExist:
#             return Response({"detail": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

#         # Check if the user is already a member of the group
#         if SavingsGroupMember.objects.filter(savings_group=group, user_id=user_id).exists():
#             return Response({"detail": "User is already a member of the group."}, status=status.HTTP_400_BAD_REQUEST)

#         data = {
#             'user': user_id,
#             'savings_group': group_id,
#             'is_admin': False,
#         }

#         serializer = SavingsGroupMemberSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     @swagger_auto_schema(
#         method='post',
#         operation_description="Leave a savings group",
#         responses={200: "You have left the group successfully."}
#     )
#     @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
#     def leave_group(self, request, *args, **kwargs):
#         """
#         Allow the logged-in user to leave a savings group.
#         Expected JSON body:
#         {
#             "savings_group": <group_id>
#         }
#         """
#         group_id = request.data.get('savings_group')
#         user = request.user

#         if not group_id:
#             return Response({"detail": "Group ID is required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             group = SavingsGroup.objects.get(id=group_id)
#         except SavingsGroup.DoesNotExist:
#             return Response({"detail": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

#         try:
#             membership = SavingsGroupMember.objects.get(savings_group=group, user=user)
#         except SavingsGroupMember.DoesNotExist:
#             return Response({"detail": "You are not a member of this group."}, status=status.HTTP_400_BAD_REQUEST)

#         # Optional: Prevent the group creator (admin) from leaving their own group
#         if membership.is_admin and group.created_by == user:
#             return Response({"detail": "Group creator cannot leave their own group."}, status=status.HTTP_400_BAD_REQUEST)

#         membership.delete()
#         return Response({"detail": "You have left the group successfully."}, status=status.HTTP_200_OK)

#     @swagger_auto_schema(
#         method='post',
#         operation_description="Join a savings group as a member",
#         responses={200: "Joined the group successfully."}
#     )
#     @action(detail=False, methods=['post'])
#     def join_group(self, request):
#         """
#         Allow the logged-in user to join a savings group.
#         Expected JSON body:
#         {
#             "savings_group": <group_id>
#         }
#         """
#         user = request.user
#         group_id = request.data.get('savings_group')

#         if not group_id:
#             return Response({"detail": "Group ID is required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             group = SavingsGroup.objects.get(id=group_id)
#         except SavingsGroup.DoesNotExist:
#             return Response({"detail": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

#         # Check if user is already a member
#         if SavingsGroupMember.objects.filter(user=user, savings_group=group).exists():
#             return Response({"detail": "You are already a member of this group."}, status=status.HTTP_400_BAD_REQUEST)

#         SavingsGroupMember.objects.create(user=user, savings_group=group, is_admin=False)
#         return Response({"detail": "Joined the group successfully."}, status=status.HTTP_200_OK)



from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError

from savings_group.models import SavingsGroup, SavingsGroupMember
from .serializers import SavingsGroupSerializer, SavingsGroupMemberSerializer

class SavingsGroupViewSet(viewsets.ModelViewSet):
    queryset = SavingsGroup.objects.all()
    serializer_class = SavingsGroupSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of savings groups",
        responses={200: SavingsGroupSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new savings group",
        responses={201: SavingsGroupSerializer},
    )
    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.id
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class SavingsGroupMemberViewSet(viewsets.ModelViewSet):
    serializer_class = SavingsGroupMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_groups = SavingsGroupMember.objects.filter(user=user).values_list('savings_group_id', flat=True)
        return SavingsGroupMember.objects.filter(savings_group_id__in=user_groups)

    @swagger_auto_schema(
        operation_description="List members of the user's savings groups",
        responses={200: SavingsGroupMemberSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new savings group member",
        responses={201: SavingsGroupMemberSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        method='post',
        operation_description="Add a new member to a savings group",
        responses={201: SavingsGroupMemberSerializer},
    )
    @action(detail=False, methods=['post'], url_path='add_member')  # url_path added
    def add_member(self, request, *args, **kwargs):
        group_id = request.data.get('savings_group')
        user_id = request.data.get('user_id')

        try:
            group = SavingsGroup.objects.get(id=group_id)
        except SavingsGroup.DoesNotExist:
            return Response({"detail": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

        if SavingsGroupMember.objects.filter(savings_group=group, user_id=user_id).exists():
            return Response({"detail": "User is already a member of the group."}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'user': user_id,
            'savings_group': group_id,
            'is_admin': False,
        }

        serializer = SavingsGroupMemberSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method='post',
        operation_description="Leave a savings group",
        responses={200: "You have left the group successfully."}
    )
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated], url_path='leave_group')  
    def leave_group(self, request, *args, **kwargs):
        group_id = request.data.get('savings_group')
        user = request.user

        if not group_id:
            return Response({"detail": "Group ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = SavingsGroup.objects.get(id=group_id)
        except SavingsGroup.DoesNotExist:
            return Response({"detail": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            membership = SavingsGroupMember.objects.get(savings_group=group, user=user)
        except SavingsGroupMember.DoesNotExist:
            return Response({"detail": "You are not a member of this group."}, status=status.HTTP_400_BAD_REQUEST)

        if membership.is_admin and group.created_by == user:
            return Response({"detail": "Group creator cannot leave their own group."}, status=status.HTTP_400_BAD_REQUEST)

        membership.delete()
        return Response({"detail": "You have left the group successfully."}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method='post',
        operation_description="Join a savings group as a member",
        responses={200: "Joined the group successfully."}
    )
    @action(detail=False, methods=['post'], url_path='join_group')  
    def join_group(self, request):
        user = request.user
        group_id = request.data.get('savings_group')

        if not group_id:
            return Response({"detail": "Group ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = SavingsGroup.objects.get(id=group_id)
        except SavingsGroup.DoesNotExist:
            return Response({"detail": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

        if SavingsGroupMember.objects.filter(user=user, savings_group=group).exists():
            return Response({"detail": "You are already a member of this group."}, status=status.HTTP_400_BAD_REQUEST)

        SavingsGroupMember.objects.create(user=user, savings_group=group, is_admin=False)
        return Response({"detail": "Joined the group successfully."}, status=status.HTTP_200_OK)
