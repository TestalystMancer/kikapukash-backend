from django.contrib import admin
from .models import CustomUser, SavingsGroup, SavingsGroupMember, Wallet, Transaction, WithdrawalRequest, Notification

# Register your models here
admin.site.register(CustomUser)
admin.site.register(SavingsGroup)
admin.site.register(SavingsGroupMember)
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(WithdrawalRequest)
admin.site.register(Notification)
