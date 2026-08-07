from pydantic import BaseModel


class CitizenComplaint(BaseModel):
    complaint: str