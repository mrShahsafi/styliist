from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from wallet.serializers import WalletDetailSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id",)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "created_date",
            "updated_date",
            "is_active",
            "is_deleted",
        )


# sometimes we need user and her/his profile at the same time but not always
class UserDetailWithWalletSerializer(serializers.ModelSerializer):

    wallet = WalletDetailSerializer(
        read_only=True,
    )

    class Meta:
        model = User
        fields = "__all__"


class UserInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "email",
            "password",
            "id",
        )

    def validate(self, attrs):
        return attrs


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]
