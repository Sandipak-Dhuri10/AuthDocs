"""
Verification App Admin Configuration
------------------------------------
This file registers the verification-related models to the Django admin site.
It allows viewing and managing uploaded documents, verification results,
and related metadata directly from the Django Admin dashboard.
"""

from django.contrib import admin
from .models import VerificationRecord


@admin.register(VerificationRecord)
class VerificationRecordAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the VerificationRecord model.
    Displays document information, verification scores, and status.
    """

    # Fields to display in the admin list view
    list_display = (
        "id",
        "user",
        "aadhaar_number",
        "status",
        "final_score",
        "result",
        "created_at",
    )

    # Fields that can be searched in the admin
    search_fields = (
        "user__username",
        "aadhaar_number",
        "result",
    )

    # Filters in the right-hand sidebar
    list_filter = (
        "status",
        "result",
        "created_at",
    )

    # Make recent documents appear first
    ordering = ("-created_at",)

    # Read-only fields (useful for immutable data)
    readonly_fields = (
        "created_at",
    )

    # Customize detail view layout
    fieldsets = (
        ("User & Document Information", {
            "fields": ("user", "aadhaar_number", "document", "template", "status"),
        }),
        ("Verification Results", {
            "fields": (
                "verhoeff_score",
                "layout_score",
                "text_score",
                "copy_move_score",
                "metadata_score",
                "ela_score",
                "final_score",
                "result",
            ),
        }),
        ("Timestamps", {
            "fields": ("created_at",),
        }),
    )
