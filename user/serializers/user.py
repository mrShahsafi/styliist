from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "full_name")


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "created_date",
            "updated_date",
            "is_deleted",
            "is_staff",
        )


class UserInputSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(
        read_only=True,
    )

    class Meta:
        model = User
        exclude = (
            "last_login",
            "is_deleted",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
        )

    def validate_password(self, value):
        validate_password(value)  # Enforces Django's password policies
        return value

    def validate(self, attrs):
        return attrs


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]
