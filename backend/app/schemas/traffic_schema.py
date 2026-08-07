from pydantic import BaseModel


class TrafficInput(BaseModel):

    city: str

    date: str

    time: str