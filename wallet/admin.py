from django.contrib import admin
from .models import Wallet

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner_type', 'owner_id', 'balance', 'created_at', 'updated_at')
    list_filter = ('owner_type', 'created_at')
    search_fields = ('owner_id',)
    ordering = ('-created_at',)
