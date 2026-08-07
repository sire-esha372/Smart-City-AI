from fastapi import APIRouter
from sqlalchemy.orm import Session

from ..database.database import SessionLocal
from ..database.models import Prediction

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/latest")
def latest_dashboard():

    db: Session = SessionLocal()

    try:

        modules = [
            "Traffic",
            "Energy",
            "Pollution",
            "Emergency",
            "Waste"
        ]

        data = {}

        for module in modules:

            latest = (
                db.query(Prediction)
                .filter(Prediction.module == module)
                .order_by(Prediction.id.desc())
                .first()
            )

            if latest:

                data[module.lower()] = {
                    "status": latest.status,
                    "value": latest.value,
                    "time": latest.timestamp
                }

            else:

                data[module.lower()] = {
                    "status": "N/A",
                    "value": "--",
                    "time": "--"
                }

        return data

    finally:
        db.close()