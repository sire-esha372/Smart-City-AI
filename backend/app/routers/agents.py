from fastapi import APIRouter

from ..schemas.agent_schema import AgentRequest

from ..agents.traffic_agent import traffic_agent
from ..agents.energy_agent import energy_agent
from ..agents.waste_agent import waste_agent
from ..agents.emergency_agent import emergency_agent
from ..config import GROQ_API_KEY

router = APIRouter(
    prefix="/agents",
    tags=["AI Agents"]
)



@router.post("/chat")
def chat(request: AgentRequest):

    agent = request.agent.lower()

    if agent == "traffic":
        answer = traffic_agent(request.query, GROQ_API_KEY)

    elif agent == "energy":
        answer = energy_agent(request.query, GROQ_API_KEY)

    elif agent == "waste":
        answer = waste_agent(request.query, GROQ_API_KEY)

    elif agent == "emergency":
        answer = emergency_agent(request.query, GROQ_API_KEY)

    else:
        answer = "Invalid Agent Selected."

    return {
        "agent": request.agent,
        "response": answer
    }