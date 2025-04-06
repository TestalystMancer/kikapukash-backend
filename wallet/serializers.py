from rest_framework import serializers
from .models import Wallet, Transaction, WithdrawalRequest, UserBalance
from django.contrib.auth import get_user_model
from savings_group.models import SavingsGroup
from users.serializers import UserSerializer  # Make sure you have this
from savings_group.serializers import SavingsGroupSerializer  # Create if not already done
from users.models import CustomUser

User = get_user_model()

class WalletSerializer(serializers.ModelSerializer):
    owner_object = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = [
            'id', 'balance', 'owner_type', 'owner_id',
            'owner_object',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['balance', 'created_at', 'updated_at']

    def get_owner_object(self, obj):
        if obj.owner_type == 'user':
            try:
                user = CustomUser.objects.get(id=obj.owner_id)
                return UserSerializer(user).data
            except CustomUser.DoesNotExist:
                return None
        elif obj.owner_type == 'savings_group':
            try:
                group = SavingsGroup.objects.get(id=obj.owner_id)
                return SavingsGroupSerializer(group).data
            except SavingsGroup.DoesNotExist:
                return None
        return None



class TransactionSerializer(serializers.ModelSerializer):
    from_wallet = serializers.PrimaryKeyRelatedField(read_only=True)
    to_wallet = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'transaction_type', 'amount', 'from_wallet', 'to_wallet', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class WithdrawalRequestSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    approved_at = serializers.DateTimeField(read_only=True)
    approved_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = WithdrawalRequest
        fields = [
            'id',
            'requester_wallet',
            'requested_savings_group_wallet',
            'amount',
            'status',
            'approved_at',
            'approved_by',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['status', 'approved_at', 'approved_by', 'created_at', 'updated_at']


class UserBalanceSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    savings_group = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserBalance
        fields = ['id', 'user', 'savings_group', 'balance']