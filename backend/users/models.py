from django.db import models
from django.contrib.auth.models import User

"""
User Model Overview:
--------------------
We are currently using Django's default User model for authentication.
If later you need to extend it (for org-level users, etc.), you can
switch to a custom user model and update AUTH_USER_MODEL in settings.py.
"""

# Example extension model (optional)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Example field for future (organization, role, etc.)
    # organization = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username
