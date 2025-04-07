from django.db import models
from common.models import TimeStampModel
from django.conf import settings
from .engines import WithdrawalRuleEngine
from django.core.exceptions import ValidationError
from django.utils import timezone

class Wallet(TimeStampModel):
    OWNER_TYPES = (
        ("user", "user"),
        ("savings_group", "savings_group"),
    )

    balance = models.PositiveBigIntegerField(default=0)
    owner_type = models.CharField(choices=OWNER_TYPES, max_length=20)
    owner_id = models.PositiveIntegerField()


class Transaction(TimeStampModel):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    ]
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    from_wallet = models.ForeignKey(Wallet, related_name='from_wallet', on_delete=models.CASCADE)
    to_wallet = models.ForeignKey(Wallet, related_name='to_wallet', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} of {self.amount} from {self.from_wallet.owner_type} to {self.to_wallet.owner_type}"


class WithdrawalRequest(TimeStampModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    requester_wallet = models.ForeignKey(Wallet, related_name='requester_wallet', on_delete=models.CASCADE)
    requested_savings_group_wallet = models.ForeignKey(Wallet, related_name='savings_wallet_group', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Request for {self.amount} - {self.status.capitalize()}"
    

    def approve(self, approved_by):
        from_wallet = self.requested_savings_group_wallet
        to_wallet = self.requester_wallet

        engine = WithdrawalRuleEngine(
            user=self.requester_wallet.owner_id,  # assuming it's a user
            group=self.requested_savings_group_wallet.owner_id,
            amount=self.amount
        )
        
        engine.validate()  # Raises ValidationError if any rule is violated

        # If validation passed, create a transaction
        Transaction.objects.create(
            type='withdrawal',
            amount=self.amount,
            from_wallet=from_wallet,
            to_wallet=to_wallet
        )

        self.status = 'approved'
        self.approved_by = approved_by
        self.approved_at = timezone.now()
        self.save()

        
from django.db import models
from django.contrib.postgres.fields import JSONField  # If using PostgreSQL
from common.models import TimeStampModel

class WithdrawalRule(TimeStampModel):
    RULE_TYPE_CHOICES = [
        ('exact', 'Exact Contribution'),
        ('time_based', 'Time-based Contribution'),
        ('flexible', 'Flexible Withdrawal'),
        ('min_balance', 'Minimum Balance Requirement'),
        ('dividend_static', 'Static Percentage Dividend'),
        ('dividend_ratio', 'Dividend by Contribution Ratio'),
        ('custom', 'Custom (JSON-defined)'),
    ]

    savings_group = models.OneToOneField(
        'savings_group.SavingsGroup',
        on_delete=models.CASCADE,
        related_name='withdrawal_rule'
    )
    
    rule_type = models.CharField(
        max_length=30,
        choices=RULE_TYPE_CHOICES,
        help_text="Type of withdrawal rule logic to apply"
    )
    
    # Optional fixed dividend payout per user contribution
    static_dividend_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text="Static percentage (e.g., 5.00 means 5%) for dividends"
    )

    # Minimum group balance to maintain even after withdrawal
    min_group_balance = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        help_text="Group wallet must retain at least this amount"
    )

    # Cap the percentage a user can withdraw
    max_withdrawal_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text="Maximum percent of wallet balance a user can withdraw"
    )

    # Restrict withdrawal to not exceed personal contribution
    restrict_to_contribution = models.BooleanField(
        default=False,
        help_text="If True, user can't withdraw more than they've contributed"
    )

    # Minimum duration user must stay in group before withdrawal
    min_membership_days = models.PositiveIntegerField(
        default=0,
        help_text="Minimum number of days a user must be a group member to withdraw"
    )

    # For advanced custom rules stored as JSON (e.g., complex logic or time rules)
    custom_rule_data = models.JSONField(  # Updated to use django.db.models.JSONField
        null=True, blank=True,
        help_text="Optional field for storing custom logic or conditions"
    )

    rule_description = models.TextField(
        help_text="Human-readable description of the rule"
    )

    def __str__(self):
        return f"Withdrawal Rule for {self.savings_group.group_name}"


class UserBalance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    savings_group = models.ForeignKey('savings_group.SavingsGroup', on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    @classmethod
    def get_or_create_balance(cls, user_id, group_id):
        obj, created = cls.objects.get_or_create(
            user_id=user_id,
            savings_group_id=group_id
        )
        return obj

    def update_balance(self, transaction_amount, transaction_type):
        if transaction_type == 'deposit':
            self.balance += transaction_amount
        elif transaction_type == 'withdrawal':
            self.balance -= transaction_amount
        self.save()
