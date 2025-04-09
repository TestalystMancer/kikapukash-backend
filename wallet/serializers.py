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



from django.db import transaction as db_transaction
from rest_framework import serializers
from wallet.models import Wallet, Transaction, UserBalance
from savings_group.serializers import SavingsGroupSerializer 
from users.serializers import UserSerializer  
from savings_group.models import SavingsGroup 

class TransactionSerializer(serializers.ModelSerializer):
    from_wallet = serializers.PrimaryKeyRelatedField(
        queryset=Wallet.objects.all(), required=False, allow_null=True)
    to_wallet = serializers.PrimaryKeyRelatedField(
        queryset=Wallet.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_type', 'amount',
            'from_wallet', 'to_wallet',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        # Validate required wallets and balance constraints per transaction type
        transaction_type = data.get('transaction_type')
        from_wallet = data.get('from_wallet')
        to_wallet = data.get('to_wallet')
        amount = data.get('amount')

        # Deposit: must have to_wallet and no from_wallet supplied.
        if transaction_type == 'deposit':
            if not to_wallet:
                raise serializers.ValidationError("Deposit must include 'to_wallet'.")
            if from_wallet:
                raise serializers.ValidationError("Deposit should not include 'from_wallet'.")
        # Withdrawal: must have from_wallet and no to_wallet; check sufficient balance.
        elif transaction_type == 'withdrawal':
            if not from_wallet:
                raise serializers.ValidationError("Withdrawal must include 'from_wallet'.")
            if to_wallet:
                raise serializers.ValidationError("Withdrawal should not include 'to_wallet'.")
            if from_wallet.balance < amount:
                raise serializers.ValidationError("Insufficient balance for withdrawal.")
        # Transfer: must include both wallets, must be distinct and have enough funds.
        elif transaction_type == 'transfer':
            if not from_wallet or not to_wallet:
                raise serializers.ValidationError("Transfer must include both 'from_wallet' and 'to_wallet'.")
            if from_wallet == to_wallet:
                raise serializers.ValidationError("Cannot transfer to the same wallet.")
            if from_wallet.balance < amount:
                raise serializers.ValidationError("Insufficient balance for transfer.")
        else:
            raise serializers.ValidationError("Invalid transaction type.")

        return data

    def create(self, validated_data):
        """
        Override create method to:
         - Persist the Transaction object.
         - Update wallet balances accordingly.
         - Update user balances if applicable.
         
        The operation is wrapped in an atomic transaction to ensure that
        all related changes succeed or none at all, maintaining data consistency.
        """
        # Use an atomic block for consistency across related updates.
        with db_transaction.atomic():
            # Create the transaction record in the database.
            transaction_obj = Transaction.objects.create(**validated_data)

            amount = transaction_obj.amount
            transaction_type = transaction_obj.transaction_type
            from_wallet = transaction_obj.from_wallet
            to_wallet = transaction_obj.to_wallet

            # Define a helper to update wallet balances safely.
            def adjust_wallet_balance(wallet, delta):
                if wallet is not None:
                    wallet.balance += delta
                    wallet.save()

            # Process deposit transactions.
            if transaction_type == 'deposit':
                # For deposits, funds are added to the destination wallet.
                if to_wallet.owner_type == 'user':
                    adjust_wallet_balance(to_wallet, amount)

                    # If the deposit originates from a savings group wallet,
                    # subtract funds from that wallet and update corresponding user balance.
                    if from_wallet is not None and from_wallet.owner_type == 'savings_group':
                        adjust_wallet_balance(from_wallet, -amount)
                        user_balance = UserBalance.get_or_create_balance(
                            user_id=to_wallet.owner_id,
                            group_id=from_wallet.owner_id
                        )
                        user_balance.update_balance(amount, 'deposit')

                elif to_wallet.owner_type == 'savings_group':
                    # When depositing into a savings group wallet, the funds usually come from a user's wallet.
                    if from_wallet is not None and from_wallet.owner_type == 'user':
                        adjust_wallet_balance(to_wallet, amount)
                        adjust_wallet_balance(from_wallet, -amount)
                        user_balance = UserBalance.get_or_create_balance(
                            user_id=from_wallet.owner_id,
                            group_id=to_wallet.owner_id
                        )
                        user_balance.update_balance(amount, 'deposit')

            # Process withdrawal transactions.
            elif transaction_type == 'withdrawal':
                if from_wallet.owner_type == 'savings_group':
                    # Withdrawing from a savings group wallet to a user's wallet.
                    if to_wallet is not None and to_wallet.owner_type == 'user':
                        adjust_wallet_balance(from_wallet, -amount)
                        adjust_wallet_balance(to_wallet, amount)
                        user_balance = UserBalance.get_or_create_balance(
                            user_id=to_wallet.owner_id,
                            group_id=from_wallet.owner_id
                        )
                        user_balance.update_balance(amount, 'withdrawal')
                elif from_wallet.owner_type == 'user':
                    # Withdrawing from a user's wallet (typically an external withdrawal).
                    adjust_wallet_balance(from_wallet, -amount)
                    # If funds are transferred into a savings group wallet, update that wallet and user balance.
                    if to_wallet is not None and to_wallet.owner_type == 'savings_group':
                        adjust_wallet_balance(to_wallet, amount)
                        user_balance = UserBalance.get_or_create_balance(
                            user_id=from_wallet.owner_id,
                            group_id=to_wallet.owner_id
                        )
                        user_balance.update_balance(amount, 'deposit')

            # Process transfer transactions.
            elif transaction_type == 'transfer':
                # Example logic for transfers:
                # Deduct from the originating wallet and add to the receiving wallet.
                adjust_wallet_balance(from_wallet, -amount)
                adjust_wallet_balance(to_wallet, amount)
                # Optionally, include any further business logic if transfers need additional processing.

            # Return the newly created transaction instance.
            return transaction_obj


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