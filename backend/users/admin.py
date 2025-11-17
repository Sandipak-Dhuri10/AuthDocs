"""
Users App Admin Configuration
------------------------------
Registers the User model to the Django admin panel with a customized view.
Handles both default Django User and custom user models gracefully.
"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Retrieve the active user model (custom or default)
User = get_user_model()

# ✅ Unregister the default User admin (to prevent AlreadyRegistered error)
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """
    Custom admin configuration for User model.
    Extends the default Django UserAdmin with clean layout and filters.
    """

    # Fields displayed in the admin user list view
    list_display = ("username", "email", "is_active", "is_staff", "is_superuser")
    list_filter = ("is_active", "is_staff", "is_superuser", "groups")

    # Editable directly from list view
    list_editable = ("is_active",)

    # Fields searchable from the admin bar
    search_fields = ("username", "email")

    # Default ordering
    ordering = ("id",)

    # Fieldsets (edit form)
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fieldsets (add form)
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "is_staff", "is_superuser"),
        }),
    )
