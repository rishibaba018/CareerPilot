from rest_framework import serializers

from .models import Resume


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ("id", "ats_score", "is_master", "parsed_text", "created_at")
        read_only_fields = fields
