from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from savings_group.models import SavingsGroup
from .serializers import SavingsGroupSerializer

class SavingsGroupViewSet(viewsets.ModelViewSet):
    queryset = SavingsGroup.objects.all()  # Retrieve all savings groups
    serializer_class = SavingsGroupSerializer  # Use the serializer defined earlier
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access the viewset
