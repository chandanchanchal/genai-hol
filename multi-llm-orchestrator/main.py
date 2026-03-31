from fastapi import FastAPI
from app.api.routes_chat import router as chat_router

app = FastAPI(title="Multi-LLM Orchestrator")

app.include_router(chat_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}
