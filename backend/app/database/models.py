from sqlalchemy import Column, Integer, String
from .database import Base


class Prediction(Base):

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    module = Column(String)

    status = Column(String)

    value = Column(String)

    timestamp = Column(String)