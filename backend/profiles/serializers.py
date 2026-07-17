from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "email",
            "full_name",
            "phone",
            "location",
            "skills",
            "education",
            "experience",
            "projects",
            "preferences",
            "updated_at",
        )
        read_only_fields = ("id", "email", "updated_at")
