from django.db import models
from django.conf import settings
from common.models import TimeStampModel
from users.models import CustomUser
# Savings Group Model
class SavingsGroup(TimeStampModel):
    group_name = models.CharField(max_length=100)
    description = models.TextField()
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.group_name

# Savings Group Membership (tracks users' roles in the group)
class SavingsGroupMember(TimeStampModel):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('member', 'Member'),
    ]
    savings_group = models.ForeignKey(SavingsGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.role} in {self.savings_group.group_name}"

# Wallet Model (used for both user and group wallets)
class Wallet(TimeStampModel):
    WALLET_OWNER_CHOICES = [
        ('user', 'User'),
        ('group', 'Group'),
    ]
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    wallet_owner_type = models.CharField(max_length=5, choices=WALLET_OWNER_CHOICES)
    wallet_owner_id = models.IntegerField()

    def __str__(self):
        return f"{self.wallet_owner_type.capitalize()} Wallet - {self.wallet_owner_id}"

# Transaction Model (tracks deposits and withdrawals)
class Transaction(TimeStampModel):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    ]
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    from_wallet = models.ForeignKey(Wallet, related_name='from_wallet', on_delete=models.CASCADE)
    to_wallet = models.ForeignKey(Wallet, related_name='to_wallet', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.type.capitalize()} of {self.amount} from {self.from_wallet.wallet_owner_type} to {self.to_wallet.wallet_owner_type}"

# Withdrawal Request Model (tracks withdrawal requests and status)
class WithdrawalRequest(TimeStampModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    requester_wallet = models.ForeignKey(Wallet, related_name='requester_wallet', on_delete=models.CASCADE)
    savings_wallet_group = models.ForeignKey(Wallet, related_name='savings_wallet_group', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Request for {self.amount} - {self.status.capitalize()}"

# Notification Model (for sending notifications to users)
class Notification(TimeStampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user}: {self.message}"
 
