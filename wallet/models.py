from django.db import models
from common.models import TimeStampModel


class Wallet(TimeStampModel):
    OWNER_TYPES = (
        ("user", "user"),
        ("savings_group", "savings_group"),
    )

    balance = models.PositiveBigIntegerField(default=0)
    owner_type = models.CharField(choices=OWNER_TYPES, max_length=20)
    owner_id = models.PositiveIntegerField()

    