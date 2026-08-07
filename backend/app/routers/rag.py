from fastapi import APIRouter

from ..schemas.rag_schema import QuestionRequest
from ..services.rag_service import ask_question
from ..config import GROQ_API_KEY

router = APIRouter(
    prefix="/rag",
    tags=["Knowledge Base"]
)




@router.post("/ask")
def ask(data: QuestionRequest):

    answer = ask_question(
        data.question,
        GROQ_API_KEY
    )

    return {
        "answer": answer
    }