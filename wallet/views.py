from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Wallet
from .serializers import WalletSerializer

class WalletViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows wallets to be viewed or edited.
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users
    filterset_fields = ['owner_type', 'owner_id']

    @swagger_auto_schema(
        operation_summary="List all wallets",
        operation_description="Retrieve a list of all wallets.",
        responses={200: WalletSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new wallet",
        operation_description="Create a new wallet with specified owner_type and owner_id.",
        responses={201: WalletSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a wallet",
        operation_description="Get the details of a wallet by ID.",
        responses={200: WalletSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a wallet",
        operation_description="Update the details of a wallet.",
        responses={200: WalletSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a wallet",
        operation_description="Partially update a wallet's information.",
        responses={200: WalletSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a wallet",
        operation_description="Delete a wallet by ID.",
        responses={204: 'No content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
