"""
Verification App URL Configuration
----------------------------------
Defines URL endpoints for document verification features.
Connects verification-related API requests from the frontend
to the corresponding Django REST framework views.
"""

from django.urls import path
from . import views

urlpatterns = [
    # POST: /api/verify/aadhaar/
    # Handles Aadhaar document upload and verification
    path("aadhaar/", views.AadhaarVerificationView.as_view(), name="aadhaar-verification"),

    # GET: /api/verify/results/<int:pk>/
    # Fetch specific verification result by ID (optional)
    path("results/<int:pk>/", views.VerificationResultView.as_view(), name="verification-result"),

    # GET: /api/verify/all/
    # Retrieve all verification records for the logged-in user (optional)
    #path("all/", views.UserVerificationListView.as_view(), name="user-verification-list"),
]
