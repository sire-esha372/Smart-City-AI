from sqlalchemy.orm import Session
from datetime import datetime

from .models import Prediction


def save_prediction(
    db: Session,
    module: str,
    status: str,
    value: str,
):
    print(f"Saving -> {module} | {status} | {value}")

    prediction = Prediction(
        module=module,
        status=status,
        value=value,
        timestamp=datetime.now().strftime("%d-%m-%Y %I:%M %p"),
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    print("Saved successfully!")

    return prediction


def get_recent_predictions(db: Session, limit: int = 10):
    return (
        db.query(Prediction)
        .order_by(Prediction.id.desc())
        .limit(limit)
        .all()
    )