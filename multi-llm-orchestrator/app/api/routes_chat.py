from fastapi import APIRouter
from app.api.schemas import ChatRequest, ChatResponse
from app.core.orchestrator import Orchestrator

router = APIRouter()
orchestrator = Orchestrator()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = orchestrator.handle_request(request)
    return result
