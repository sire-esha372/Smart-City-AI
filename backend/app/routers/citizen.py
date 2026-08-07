from fastapi import APIRouter

from ..schemas.citizen_schema import CitizenComplaint
from ..services.citizen_service import summarize_complaint

router = APIRouter(
    prefix="/citizen",
    tags=["Citizen Services"]
)


@router.post("/summarize")
def citizen(data: CitizenComplaint):
    return summarize_complaint(data)