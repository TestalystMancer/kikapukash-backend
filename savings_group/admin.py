from django.contrib import admin
from .models import SavingsGroup

@admin.register(SavingsGroup)
class SavingsGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'target_amount', 'created_by', 'created_at', 'updated_at')
    search_fields = ('group_name', 'description', 'created_by__email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
