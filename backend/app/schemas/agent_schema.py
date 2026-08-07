from pydantic import BaseModel


class AgentRequest(BaseModel):
    agent: str
    query: str