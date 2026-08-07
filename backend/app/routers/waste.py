from fastapi import APIRouter, UploadFile, File

from ..services.waste_service import predict_waste

router = APIRouter(
    prefix="/predict",
    tags=["Waste Classification"]
)


@router.post("/waste")
async def waste_prediction(file: UploadFile = File(...)):

    result = predict_waste(file.file)

    return result