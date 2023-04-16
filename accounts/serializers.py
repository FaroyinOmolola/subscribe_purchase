from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    created_at = serializers.DateTimeField(source="date_joined", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_staff",
            "created_at",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name") or "",
            last_name=validated_data.get("last_name") or "",
            is_staff=validated_data.get("is_staff") or False,
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
