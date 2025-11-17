import requests
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .models import VerificationRecord
from .utils.scoring import calculate_final_score
from .serializers import VerificationRecordSerializer


class AadhaarVerificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        POST /api/verify/aadhaar/
        Payload:
            aadhaar_number: "123456789012"
            document: <file>
            template: <file> (optional)
        """
        try:
            aadhaar_number = request.data.get("aadhaar_number")
            document = request.FILES.get("document")
            template = request.FILES.get("template", None)

            if not aadhaar_number or not document:
                return Response(
                    {"error": "Aadhaar number and document are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Step 1 — Create record
            record = VerificationRecord.objects.create(
                user=request.user,
                document=document,
                template=template,
                aadhaar_number=aadhaar_number,
                status="Processing",
            )

            # Step 2 — Prepare files for ML-service
            document.file.seek(0)
            files = {
                "document": ("document.jpg", document.file.read(), document.content_type or "image/jpeg"),
            }
            if template:
                template.file.seek(0)
                files["template"] = ("template.jpg", template.file.read(), template.content_type or "image/jpeg")

            data = {"aadhaar_number": aadhaar_number}

            # Step 3 — Send to ML-service
            ml_url = f"{settings.ML_SERVICE_URL}/verify/aadhaar"
            response = requests.post(ml_url, files=files, data=data, timeout=180)

            if response.status_code != 200:
                record.status = "Error"
                record.save()
                return Response(
                    {"error": "ML-service returned an error.", "details": response.text},
                    status=response.status_code,
                )

            # Step 4 — Process ML response
            ml_data = response.json()
            results = calculate_final_score(ml_data)

            final_score_raw = results["final_score"]        # normalized 0–1
            classification = results["classification"]

            # Step 5 — Save to DB (keep 0–1 for DB)
            record.verhoeff_score = ml_data.get("verhoeff")
            record.layout_score = ml_data.get("layout")
            record.text_score = ml_data.get("text")
            record.copy_move_score = ml_data.get("copy_move")
            record.metadata_score = ml_data.get("metadata")
            record.ela_score = ml_data.get("ela")
            record.final_score = final_score_raw
            record.result = classification
            record.status = "Completed"
            record.save()

            # Step 6 — Respond to frontend (scale 0–100)
            return Response(
                {
                    "aadhaar_number": aadhaar_number,
                    "scores": {
                        "verhoeff": (ml_data.get("verhoeff", 0) or 0) * 100,
                        "layout": (ml_data.get("layout", 0) or 0) * 100,
                        "text": (ml_data.get("text", 0) or 0) * 100,
                        "copy_move": (ml_data.get("copy_move", 0) or 0) * 100,
                        "metadata": (ml_data.get("metadata", 0) or 0) * 100,
                        "ela": (ml_data.get("ela", 0) or 0) * 100,
                    },
                    "final_score": round(final_score_raw * 100, 2),
                    "classification": classification,
                    "status": "Completed",
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            print(f"[Error] Aadhaar verification failed: {e}")
            return Response(
                {"error": f"Unexpected error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class VerificationResultView(generics.RetrieveAPIView):
    """
    Retrieve a completed verification record by ID.
    """
    queryset = VerificationRecord.objects.all()
    serializer_class = VerificationRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except VerificationRecord.DoesNotExist:
            return Response(
                {"error": "Result not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
