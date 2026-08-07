from pydantic import BaseModel

class PowerInput(BaseModel):
    date: str
    time: str