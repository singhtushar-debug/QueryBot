from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.agenticAI.graph.graph import app

router = APIRouter()


class ChatRequest(BaseModel):
    """Incoming chat request from the user."""

    message: str = Field(..., description="The user query.")


@router.post("/")
def chat(request: ChatRequest):
    initial_state = {
        "message": [{"role":"user","content":request.message}]
    }
  
    res = app.invoke(initial_state)

    return {
        "response": res.get("final_response", "Sorry, I couldn't process your request.")
    }
