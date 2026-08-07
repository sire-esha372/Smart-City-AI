from pydantic import BaseModel


class PollutionInput(BaseModel):
    city: str