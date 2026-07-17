from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    full_name = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "full_name")
        read_only_fields = ("id",)

    def create(self, validated_data):
        full_name = validated_data.pop("full_name", "")
        user = User.objects.create_user(**validated_data)
        # Every user gets an empty master profile at signup
        from profiles.models import Profile

        Profile.objects.create(user=user, full_name=full_name)
        return user


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="profile.full_name", read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "full_name", "created_at")
