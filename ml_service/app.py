from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from concurrent.futures import ThreadPoolExecutor
import uvicorn
import os

# Import all verifiers and utilities
from verifiers.verhoeff import verhoeff_check
from verifiers.layout_check import layout_similarity
from verifiers.text_check import text_match
from verifiers.copy_move import copy_move_detection
from verifiers.metadata_check import metadata_analysis
from verifiers.ela_check import ela_analysis
from utils.helpers import save_temp_file

# ===============================
# Initialize FastAPI app
# ===============================
app = FastAPI(
    title="AuthDoc ML-Service",
    description="Performs document forgery checks on uploaded Aadhaar documents.",
    version="1.0.0"
)

# ===============================
# Thread Pool for Parallel Execution
# ===============================
executor = ThreadPoolExecutor(max_workers=6)


# ===============================
# Route: Aadhaar Verification
# ===============================
@app.post("/verify/aadhaar")
async def verify_aadhaar(
    aadhaar_number: str = Form(...),
    document: UploadFile = None,
    template: UploadFile = None
):
    """
    Receives an Aadhaar image and template, performs multiple forgery checks,
    and returns metric scores in JSON format.
    """

    if not aadhaar_number or not document:
        return JSONResponse(
            {"error": "Missing Aadhaar number or document file."},
            status_code=400
        )

    # Save temporary files
    doc_path = save_temp_file(document)
    template_path = save_temp_file(template) if template else None

    try:
        # Prepare verification tasks to run in parallel
        tasks = {
            "verhoeff": executor.submit(verhoeff_check, aadhaar_number),
            "layout": executor.submit(layout_similarity, doc_path, template_path),
            "text": executor.submit(text_match, doc_path, aadhaar_number),
            "copy_move": executor.submit(copy_move_detection, doc_path),
            "metadata": executor.submit(metadata_analysis, doc_path),
            "ela": executor.submit(ela_analysis, doc_path)
        }

        # Collect results from all verifiers
        results = {}
        for name, task in tasks.items():
            try:
                results[name] = round(task.result(timeout=120), 3)
            except Exception as e:
                results[name] = 0.0  # Default to 0 if a module fails
                print(f"[Warning] {name} check failed: {e}")

        # Cleanup temporary files
        if os.path.exists(doc_path):
            os.remove(doc_path)
        if template_path and os.path.exists(template_path):
            os.remove(template_path)

        # Return results as JSON
        return JSONResponse(results, status_code=200)

    except Exception as e:
        print(f"[Error] Verification failed: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# ===============================
# Root Endpoint
# ===============================
@app.get("/")
def root():
    return {"message": "AuthDoc ML-Service is running successfully."}


# ===============================
# Run (only for standalone testing)
# ===============================
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
