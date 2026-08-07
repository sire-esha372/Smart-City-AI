from fastapi import APIRouter
from sqlalchemy.orm import Session

from ..database.database import SessionLocal
from ..database.models import Prediction

router = APIRouter(
    prefix="/history",
    tags=["Prediction History"]
)


@router.get("/")
def prediction_history():

    db: Session = SessionLocal()

    try:

        predictions = (
            db.query(Prediction)
            .order_by(Prediction.id.desc())
            .all()
        )

        return [
            {
                "id": p.id,
                "module": p.module,
                "status": p.status,
                "value": p.value,
                "timestamp": p.timestamp,
            }
            for p in predictions
        ]

    finally:
        db.close()