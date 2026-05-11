from fastapi import APIRouter
from pydantic import BaseModel,Field
from app.agenticAI.graph.graph import app

router = APIRouter()

class ChatRequest(BaseModel):
    """Incoming chat request from the user."""
    message: str = Field(...,description="The user query.")

@router.post("/")
def chat(request:ChatRequest):
    initial_state = {
        "messages": [],
        "user_query": request.message,
        "intent": None,
        "products":[],
        "agent_ouput":"",
        "final_response":"",
        "reasoning":"",
    }

    res = app.invoke(initial_state)

    return {
        "response":res.get('final_response',"Sorry, I couldn't process your request.")
    }
    