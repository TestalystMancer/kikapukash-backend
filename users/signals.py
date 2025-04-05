from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import CustomUser
from wallet.models import Wallet

@receiver(post_save, sender=CustomUser)
def create_wallet_for_user(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(
            owner_type="user",
            owner_id=instance.pk,
            balance=0 
        )
