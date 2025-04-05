# withdrawal/engines.py
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal

from savings_group.models import SavingsGroupMember, Wallet
from wallet.models import UserBalance

class WithdrawalRuleEngine:
    def __init__(self, user, group, amount):
        self.user = user
        self.group = group
        self.amount = Decimal(amount)
        self.rule = group.withdrawal_rule
        self.user_balance = UserBalance.get_or_create_balance(user_id=user.id, group_id=group.id)

    def validate(self):
        self._check_min_duration()
        self._check_min_group_balance()
        self._check_contribution_limit()
        self._check_max_withdrawal_percentage()

    def _check_min_duration(self):
        try:
            member = SavingsGroupMember.objects.get(user=self.user, savings_group=self.group)
        except SavingsGroupMember.DoesNotExist:
            raise ValidationError("User is not a member of the group.")

        days_in_group = (timezone.now() - member.created_at).days
        if days_in_group < self.rule.min_duration_in_group:
            raise ValidationError(f"Minimum duration to withdraw is {self.rule.min_duration_in_group} days.")

    def _check_min_group_balance(self):
        if self.rule.min_balance_required:
            group_wallet = Wallet.objects.get(owner_type='savings_group', owner_id=self.group.id)
            projected_balance = group_wallet.balance - self.amount
            if projected_balance < self.rule.min_balance_required:
                raise ValidationError("Withdrawal would violate minimum group balance requirement.")

    def _check_contribution_limit(self):
        if self.rule.requester_cannot_withdraw_more_than_they_put_in:
            if self.amount > self.user_balance.balance:
                raise ValidationError("You cannot withdraw more than you have contributed.")

    def _check_max_withdrawal_percentage(self):
        if self.rule.max_withdrawal_percentage:
            group_wallet = Wallet.objects.get(owner_type='savings_group', owner_id=self.group.id)
            max_allowed = (self.rule.max_withdrawal_percentage / 100) * group_wallet.balance
            if self.amount > max_allowed:
                raise ValidationError(f"Cannot withdraw more than {self.rule.max_withdrawal_percentage}% of group funds.")
