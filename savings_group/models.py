from django.db import models
from common.models import TimeStampModel
from django.conf import settings

class SavingsGroup(TimeStampModel):
    group_name = models.CharField(max_length=100)
    description = models.TextField()
    target_amount = models.PositiveBigIntegerField(default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='created_items'
    )
    