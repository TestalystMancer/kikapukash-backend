from rest_framework import serializers
from .models import SavingsGroup,SavingsGroupMember
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model


class SavingsGroupMemberSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())  
    is_admin = serializers.BooleanField(default=False)

    class Meta:
        model = SavingsGroupMember
        fields = ['user', 'is_admin']

    def validate_user(self, value):
        if SavingsGroupMember.objects.filter(savings_group=self.instance.savings_group, user=value).exists():
            raise serializers.ValidationError("This user is already a member of the group.")
        return value

    def create(self, validated_data):
        return SavingsGroupMember.objects.create(**validated_data)


class SavingsGroupSerializer(serializers.ModelSerializer):
    members = SavingsGroupMemberSerializer(many=True, read_only=True)

    class Meta:
        model = SavingsGroup
        fields = '__all__'
    
    def validate_group_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Group name must be at least 3 characters long.")
        return value