from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SavingsGroup, SavingsGroupMember
from wallet.models import Wallet, Transaction, UserBalance
from users.models import CustomUser
from notifications.models import Notification

# Notifying based on transaction type
def create_notification(user, message):
    print(f"Creating notification for user {user}: {message}")
    Notification.objects.create(user=user, message=message)

@receiver(post_save, sender=Transaction)
def update_wallet_and_user_balance(sender, instance, created, **kwargs):
    if not created:
        return

    amount = instance.amount
    transaction_type = instance.transaction_type
    from_wallet = instance.from_wallet
    to_wallet = instance.to_wallet

    # Helper function to update the wallet's balance.
    def adjust_wallet_balance(wallet, delta):
        if wallet is not None:  # Safety check: ensure wallet exists.
            wallet.balance += delta
            wallet.save()

    

    # DEPOSIT FLOW
    if transaction_type == 'deposit':
        if to_wallet is not None and to_wallet.owner_type == 'user':
            user = CustomUser.objects.get(id=to_wallet.owner_id)
            # Deposit into user's wallet (incoming funds).
            adjust_wallet_balance(to_wallet, amount)
            create_notification(user, f"Deposited {amount} into your wallet")

            # Notification.get_or_create_notification(user=user.id, message=f"You have deposited {amount} into your wallet")


            if from_wallet is not None and from_wallet.owner_type == 'savings_group':
                adjust_wallet_balance(from_wallet, -amount)

                user_balance = UserBalance.get_or_create_balance(
                    user_id=to_wallet.owner_id,
                    group_id=from_wallet.owner_type
                )
                user_balance.update_balance(amount, 'deposit')

                # Create deposit notification for the user

                Notification.get_or_create_notification(user_id=user, message=f"You have deposited {amount} into your wallet")

                create_notification(user, f"Deposited {amount} into your wallet")

        elif to_wallet is not None and to_wallet.owner_type == 'savings_group':
            user = CustomUser.objects.get(id=to_wallet.owner_id)

            if from_wallet is not None and from_wallet.owner_type == 'user':
                adjust_wallet_balance(to_wallet, amount)
                adjust_wallet_balance(from_wallet, -amount)

                user_balance = UserBalance.get_or_create_balance(
                    user_id=from_wallet.owner_type,
                    group_id=to_wallet.owner_id
                )
                user_balance.update_balance(amount, 'deposit')

                # Create deposit notification for the user
                create_notification(from_wallet.owner_id, f"Deposited {amount} into savings group")

    # WITHDRAWAL FLOW
    elif transaction_type == 'withdrawal':
        if from_wallet is not None and from_wallet.owner_type == 'savings_group':
            if to_wallet is not None and to_wallet.owner_type == 'user':
                user = CustomUser.objects.get(id=from_wallet.owner_id)

                adjust_wallet_balance(from_wallet, -amount)
                adjust_wallet_balance(to_wallet, amount)

                user_balance = UserBalance.get_or_create_balance(
                    user_id=to_wallet.owner_id,
                    group_id=from_wallet.owner_type_type_type_type_type_id
                )
                user_balance.update_balance(amount, 'withdrawal')

                # Create withdrawal notification for the user
                create_notification(user, f"You have withdrawn {amount} from your wallet")

        elif from_wallet is not None and from_wallet.owner_type == 'user':
            user = CustomUser.objects.get(id=from_wallet.owner_id)
            create_notification(user, f"You have withdrawn {amount} from your wallet")

            adjust_wallet_balance(from_wallet, -amount)

            if to_wallet is not None and to_wallet.owner_type == 'savings_group':
                adjust_wallet_balance(to_wallet, amount)

                user_balance = UserBalance.get_or_create_balance(
                    user_id=from_wallet.owner_type,
                    group_id=to_wallet.owner_id
                )
                user_balance.update_balance(amount, 'deposit')

                # Create withdrawal notification for the user

    # Transfer flow
    elif transaction_type == 'transfer':
        if from_wallet is not None and to_wallet is not None:
            adjust_wallet_balance(from_wallet, -amount)
            adjust_wallet_balance(to_wallet, amount)
            userFrom = CustomUser.objects.get(id=from_wallet.owner_id)
            userTo = CustomUser.objects.get(id=to_wallet.owner_id)

            

            # Optionally create notifications for both sender and receiver
            create_notification(userFrom, f"Transferred {amount} to another wallet")
            create_notification(userTo, f"Received {amount} from another wallet")
