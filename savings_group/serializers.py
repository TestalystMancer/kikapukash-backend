from rest_framework import serializers
from .models import SavingsGroup,SavingsGroupMember
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model


class SavingsGroupMemberSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    is_admin = serializers.BooleanField(default=False)
    savings_group = serializers.PrimaryKeyRelatedField(queryset=SavingsGroup.objects.all())

    class Meta:
        model = SavingsGroupMember
        fields = ['user', 'is_admin', 'savings_group']

    def validate(self, data):
        user = data.get('user')
        group = data.get('savings_group')
        if SavingsGroupMember.objects.filter(savings_group=group, user=user).exists():
            raise serializers.ValidationError("This user is already a member of the group.")
        return data

    def create(self, validated_data):
        return SavingsGroupMember.objects.create(**validated_data)



class SavingsGroupSerializer(serializers.ModelSerializer):
    members = SavingsGroupMemberSerializer(many=True, read_only=True)

    class Meta:
        model = SavingsGroup
        fields = [
            'id',
            'group_name',
            'target_amount',
            'description',
            'created_by',
            'created_at',
            'updated_at',
            'members',
        ]
        read_only_fields = ['created_at', 'updated_at']  # Mark created_by as read-only

    def validate_group_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Group name must be at least 3 characters long.")
        return value
    
    # def create(self, validated_data):
    #     # Set created_by to the current user (from the viewset or request context)
    #     validated_data['created_by'] = self.context['request'].user
    #     return super().create(validated_data)

    # Add at the bottom of savings_group/serializers.py

class JoinLeaveGroupSerializer(serializers.Serializer):
    group_id = serializers.PrimaryKeyRelatedField(queryset=SavingsGroup.objects.all())

    def validate(self, data):
        user = self.context['request'].user
        group = data['group_id']
        if SavingsGroupMember.objects.filter(user=user, SavingsGroup=group).exists():
            raise ValidationError("You are already a member of this group.")
        return data
