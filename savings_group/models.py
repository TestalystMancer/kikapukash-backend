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
    
    def get_savings_group_balance():
        # calculate this by querying all the savings group members wallet
        pass

class SavingsGroupMember(TimeStampModel):
    SavingsGroup = models.ForeignKey(SavingsGroup, on_delete=models.CASCADE, related_name='members')
    User = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='group_memberships')
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.User} - {self.SavingsGroup.group_name} ({'Admin' if self.is_admin else 'Member'})"



