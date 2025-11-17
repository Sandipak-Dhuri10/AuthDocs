"""
Verification Serializers
------------------------
This module defines serializers for the VerificationRecord model,
used to convert model instances into JSON responses for the frontend.
"""

from rest_framework import serializers
from .models import VerificationRecord


class VerificationRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for VerificationRecord model.
    Converts model data into JSON format for API responses.
    """

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = VerificationRecord
        fields = [
            "id",
            "user",
            "aadhaar_number",
            "document",
            "template",
            "verhoeff_score",
            "layout_score",
            "text_score",
            "copy_move_score",
            "metadata_score",
            "ela_score",
            "final_score",
            "result",
            "status",
            "created_at",
            "updated_at",
        ]
