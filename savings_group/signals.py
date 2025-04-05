# your_app/signals/savings_group_signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SavingsGroup, SavingsGroupMember
from wallet.models import Wallet, Transaction,UserBalance

@receiver(post_save, sender=SavingsGroup)
def create_wallet_for_savings_group(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(
            owner_type="savings_group",
            owner_id=instance.pk,
            balance=0 
        )

@receiver(post_save, sender=SavingsGroup)
def add_creator_as_member(sender, instance, created, **kwargs):
    if created:
        SavingsGroupMember.objects.create(
            SavingsGroup=instance,
            User=instance.created_by,
            is_admin=True
        )

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction, Wallet, UserBalance

@receiver(post_save, sender=Transaction)
def update_wallet_and_user_balance(sender, instance, created, **kwargs):
    if not created:
        return

    amount = instance.amount
    transaction_type = instance.transaction_type
    from_wallet = instance.from_wallet
    to_wallet = instance.to_wallet

    # Helper to update wallet balances
    def adjust_wallet_balance(wallet, delta):
        wallet.balance += delta
        wallet.save()

    # Deposit flow
    if transaction_type == 'deposit':
        if to_wallet.owner_type == 'user':
            # Incoming deposit to user's wallet (either from external or group)
            adjust_wallet_balance(to_wallet, amount)

            # If from a group wallet → update group & user balance
            if from_wallet.owner_type == 'savings_group':
                adjust_wallet_balance(from_wallet, -amount)

                user_balance = UserBalance.get_or_create_balance(
                    user_id=to_wallet.owner_id,
                    group_id=from_wallet.owner_id
                )
                user_balance.update_balance(amount, 'deposit')

        elif to_wallet.owner_type == 'savings_group':
            # Deposit into group wallet (must come from user's wallet)
            adjust_wallet_balance(to_wallet, amount)
            adjust_wallet_balance(from_wallet, -amount)

            user_balance = UserBalance.get_or_create_balance(
                user_id=from_wallet.owner_id,
                group_id=to_wallet.owner_id
            )
            user_balance.update_balance(amount, 'deposit')

    # Withdrawal flow
    elif transaction_type == 'withdrawal':
        if from_wallet.owner_type == 'savings_group':
            # Withdrawal from group to user's wallet
            adjust_wallet_balance(from_wallet, -amount)
            adjust_wallet_balance(to_wallet, amount)

            user_balance = UserBalance.get_or_create_balance(
                user_id=to_wallet.owner_id,
                group_id=from_wallet.owner_id
            )
            user_balance.update_balance(amount, 'withdrawal')

        elif from_wallet.owner_type == 'user':
            # Withdrawal from user's wallet (e.g. to external)
            adjust_wallet_balance(from_wallet, -amount)

            # If it's going to a savings group → top up group wallet
            if to_wallet.owner_type == 'savings_group':
                adjust_wallet_balance(to_wallet, amount)

                user_balance = UserBalance.get_or_create_balance(
                    user_id=from_wallet.owner_id,
                    group_id=to_wallet.owner_id
                )
                user_balance.update_balance(amount, 'deposit')
