from fastapi import APIRouter, UploadFile, File
import os
import uuid

from ..services.emergency_service import detect_emergency


router = APIRouter(
    prefix="/emergency",
    tags=["Emergency Detection"]
)


@router.post("/predict")
async def predict_emergency(
    file: UploadFile = File(...)
):

    # Temporary upload directory
    upload_dir = os.path.join(
        os.path.dirname(__file__),
        "..",
        "static",
        "uploads"
    )

    os.makedirs(
        upload_dir,
        exist_ok=True
    )


    # Unique filename
    filename = (
        f"{uuid.uuid4().hex}_"
        f"{file.filename}"
    )

    image_path = os.path.join(
        upload_dir,
        filename
    )


    # Save uploaded image
    contents = await file.read()

    with open(
        image_path,
        "wb"
    ) as f:

        f.write(contents)


    # Run YOLO
    result = detect_emergency(
        image_path
    )


    return result