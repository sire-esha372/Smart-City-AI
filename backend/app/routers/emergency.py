from fastapi import APIRouter, UploadFile, File
import os
import shutil

from ..services.emergency_service import detect_emergency

router = APIRouter(
    prefix="/emergency",
    tags=["Emergency Detection"]
)

# Folder to temporarily store uploaded images
UPLOAD_FOLDER = "app/static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/predict")
async def predict_emergency(file: UploadFile = File(...)):
    # Save uploaded image
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Detect fire/smoke
    result = detect_emergency(file_path)

    return result