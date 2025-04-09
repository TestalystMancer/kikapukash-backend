from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SavingsGroup, SavingsGroupMember
from wallet.models import Wallet, Transaction, UserBalance

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
            user=instance.created_by,
            is_admin=True
        )

@receiver(post_save, sender=Transaction)
def update_wallet_and_user_balance(sender, instance, created, **kwargs):
    # Process only newly created transactions
    if not created:
        return

    amount = instance.amount
    transaction_type = instance.transaction_type
    from_wallet = instance.from_wallet  # May be None; check later before access.
    to_wallet = instance.to_wallet      # May be None; check later before access.

    # Helper function to update the wallet's balance.
    def adjust_wallet_balance(wallet, delta):
        if wallet is not None:  # Safety check: ensure wallet exists.
            wallet.balance += delta
            wallet.save()

    # DEPOSIT FLOW
    if transaction_type == 'deposit':
        # Ensure to_wallet is not None before checking its owner_type.
        if to_wallet is not None and to_wallet.owner_type == 'user':
            # Deposit into user's wallet (incoming funds).
            adjust_wallet_balance(to_wallet, amount)

            # If funds come from a savings_group wallet, make sure from_wallet is valid.
            if from_wallet is not None and from_wallet.owner_type == 'savings_group':
                adjust_wallet_balance(from_wallet, -amount)

                # Get or create the corresponding user balance and update it.
                user_balance = UserBalance.get_or_create_balance(
                    user_id=to_wallet.owner_id,
                    group_id=from_wallet.owner_id
                )
                user_balance.update_balance(amount, 'deposit')

        elif to_wallet is not None and to_wallet.owner_type == 'savings_group':
            # Deposit into a group wallet coming from a user's wallet.
            if from_wallet is not None and from_wallet.owner_type == 'user':
                adjust_wallet_balance(to_wallet, amount)
                adjust_wallet_balance(from_wallet, -amount)

                user_balance = UserBalance.get_or_create_balance(
                    user_id=from_wallet.owner_id,
                    group_id=to_wallet.owner_id
                )
                user_balance.update_balance(amount, 'deposit')
            else:
                # Optionally, log or handle unexpected missing from_wallet data here.
                pass

    # WITHDRAWAL FLOW
    elif transaction_type == 'withdrawal':
        if from_wallet is not None and from_wallet.owner_type == 'savings_group':
            # Withdrawal from a group's wallet to a user's wallet.
            if to_wallet is not None and to_wallet.owner_type == 'user':
                adjust_wallet_balance(from_wallet, -amount)
                adjust_wallet_balance(to_wallet, amount)

                user_balance = UserBalance.get_or_create_balance(
                    user_id=to_wallet.owner_id,
                    group_id=from_wallet.owner_id
                )
                user_balance.update_balance(amount, 'withdrawal')
            else:
                # Handle missing to_wallet or unexpected owner_type.
                pass

        elif from_wallet is not None and from_wallet.owner_type == 'user':
            # Withdrawal from a user's wallet, e.g., moving funds externally.
            adjust_wallet_balance(from_wallet, -amount)

            # Check if the target wallet exists and is a savings_group wallet.
            if to_wallet is not None and to_wallet.owner_type == 'savings_group':
                adjust_wallet_balance(to_wallet, amount)

                user_balance = UserBalance.get_or_create_balance(
                    user_id=from_wallet.owner_id,
                    group_id=to_wallet.owner_id
                )
                user_balance.update_balance(amount, 'deposit')
            # Otherwise, no further action if the funds go somewhere external.
