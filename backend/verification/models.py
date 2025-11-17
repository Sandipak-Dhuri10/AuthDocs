from django.db import models
from django.contrib.auth.models import User

"""
Model Purpose:
--------------
Stores uploaded document details and their verification results.
Each record represents one verification request made by a user.
"""


class VerificationRecord(models.Model):
    # User who uploaded the document
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verifications')

    # Aadhaar file (uploaded by user)
    document = models.FileField(upload_to='documents/')

    # Template file (official Aadhaar template)
    template = models.FileField(upload_to='templates/', blank=True, null=True)

    # Aadhaar number entered by user
    aadhaar_number = models.CharField(max_length=12)

    # Results from ML-service
    verhoeff_score = models.FloatField(blank=True, null=True)
    layout_score = models.FloatField(blank=True, null=True)
    text_score = models.FloatField(blank=True, null=True)
    copy_move_score = models.FloatField(blank=True, null=True)
    metadata_score = models.FloatField(blank=True, null=True)
    ela_score = models.FloatField(blank=True, null=True)

    # Final aggregated score
    final_score = models.FloatField(blank=True, null=True)

    # Classification: Authentic / Suspicious / Forged
    result = models.CharField(max_length=20, blank=True, null=True)

    # Status and timestamps
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Aadhaar: {self.aadhaar_number} ({self.result or 'Not Verified'})"
