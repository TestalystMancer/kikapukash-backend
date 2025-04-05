# your_app/signals/savings_group_signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SavingsGroup
from wallet.models import Wallet


@receiver(post_save, sender=SavingsGroup)
def create_wallet_for_savings_group(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(
            owner_type="savings_group",
            owner_id=instance.pk,
            balance=0 
        )
