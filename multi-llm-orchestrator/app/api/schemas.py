from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    user_input: str
    task_type: Optional[str] = None
    max_budget: Optional[float] = 0.05

class ChatResponse(BaseModel):
    selected_model: str
    provider: str
    response: str
    fallback_used: bool
    estimated_cost: float
