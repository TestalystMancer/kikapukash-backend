from django.contrib import admin
from .models import Wallet,Transaction

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner_type', 'owner_id', 'balance', 'created_at', 'updated_at')
    list_filter = ('owner_type', 'created_at')
    search_fields = ('owner_id',)
    ordering = ('-created_at',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'amount', 'from_wallet', 'to_wallet', 'created_at', 'updated_at')
    list_filter = ('transaction_type', 'from_wallet', 'to_wallet', 'created_at')
    search_fields = ('from_wallet__wallet_owner_type', 'to_wallet__wallet_owner_type', 'amount')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    # Optional: Add fields to inline edit the related Wallet model
    # in case you want a more customized inline form for transactions.
    # In this case, you would also create an inline model admin for Wallet.
    
    def get_queryset(self, request):
        """
        Optionally, you can customize the queryset to show only transactions related to the current user.
        """
        queryset = super().get_queryset(request)
        # Add any further custom filtering here if needed
        return queryset

admin.site.register(Transaction, TransactionAdmin)