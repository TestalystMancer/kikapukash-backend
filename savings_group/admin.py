from django.contrib import admin
from .models import SavingsGroup,SavingsGroupMember

@admin.register(SavingsGroup)
class SavingsGroupAdmin(admin.ModelAdmin):
    list_display = ('id','group_name', 'target_amount', 'created_by', 'created_at', 'updated_at')
    search_fields = ('group_name', 'description', 'created_by__email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(SavingsGroupMember)
class SavingsGroupMemberAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'SavingsGroup', 'is_admin', 'created_at', 'updated_at')
    list_filter = ('is_admin', 'SavingsGroup')
    search_fields = ('User__username', 'User__email',)
    ordering = ('-created_at',)