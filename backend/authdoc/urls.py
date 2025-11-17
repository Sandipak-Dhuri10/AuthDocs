from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # ===============================
    # Admin Panel
    # ===============================
    path('admin/', admin.site.urls),

    # ===============================
    # Authentication APIs (Users App)
    # ===============================
    path('api/auth/', include('users.urls')),

    # ===============================
    # Document Verification APIs
    # ===============================
    path('api/verify/', include('verification.urls')),

    # ===============================
    # JWT Authentication Endpoints
    # ===============================
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


# ===============================
# Media & Static File Serving
# (for uploaded Aadhaar templates, etc.)
# ===============================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
