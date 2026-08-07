from fastapi import APIRouter

from ..schemas.traffic_schema import TrafficInput
from ..services.traffic_service import predict_traffic

router = APIRouter()


@router.post("/predict/traffic")
def predict(data: TrafficInput):
    return predict_traffic(data)