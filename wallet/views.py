from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Wallet
from .serializers import WalletSerializer
from rest_framework import viewsets, permissions
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing transactions between wallets. 
    Users can view their transactions, both sent and received.
    """
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of transactions for the authenticated user, including both sent and received transactions.",
        responses={200: TransactionSerializer(many=True)}
    )
    def get_queryset(self):
        user = self.request.user
        
        # Get all Wallets owned by the user
        user_wallets = Wallet.objects.filter(owner_type='user', owner_id=user.id)
        
        # Return all transactions where the user's wallet is either the 'from_wallet' or 'to_wallet'
        return Transaction.objects.filter(from_wallet__in=user_wallets) | Transaction.objects.filter(to_wallet__in=user_wallets)

    @swagger_auto_schema(
        operation_description="Create a new transaction. The user must provide valid wallet information for sending and receiving funds.",
        request_body=TransactionSerializer,
        responses={201: TransactionSerializer}
    )
    def create(self, request, *args, **kwargs):
        """
        Handle the creation of a new transaction by the authenticated user.
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific transaction.",
        responses={200: TransactionSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve detailed information for a specific transaction by its ID.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update the details of an existing transaction.",
        request_body=TransactionSerializer,
        responses={200: TransactionSerializer}
    )
    def update(self, request, *args, **kwargs):
        """
        Update the details of an existing transaction.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific transaction by its ID.",
        responses={204: 'Transaction deleted successfully.'}
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific transaction by its ID.
        """
        return super().destroy(request, *args, **kwargs)



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
