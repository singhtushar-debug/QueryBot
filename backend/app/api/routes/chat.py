from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from app.agenticAI.graph.graph import app
import json
router = APIRouter()


class ChatRequest(BaseModel):
    """Incoming chat request from the user."""

    message: str = Field(..., description="The user query.")

config = {"configurable": {"thread_id": "1"}}

async def stream_graph_response(query: str):
    async for event in app.astream_events(
        {"messages": [{"role":"user","content":query}]},
        version= 'v2',
        config = config
    ):
        event_type = event['event']

        # Stream LLM tokens
        if event_type == "on_chat_model_stream":
            node = event.get("metadata", {}).get("langgraph_node")
            if node == "supervisor":
                chunk = event['data']['chunk']
                if chunk.content:
                    # print(f"onchat...{chunk.content}")
                    yield json.dumps({
                        "type": "content",
                        "content": chunk.content
                    }) + "\n"
        
        # Stream TOOL events
        elif event_type == "on_tool_start":
            print(event)
            yield json.dumps({
                "type": "tool_start",
                "tool": event['name']
            }) + "\n"

        elif event_type == "on_tool_end":
            print(event)
            yield json.dumps({
                "type": "tool_end",
                "tool": event['name']
            }) + "\n"

        # Stream THINKING 
        elif event_type == "on_chain_stream":
            chunk = event['data']['chunk']
            if "supervisor" in chunk:
                supervisor_data = chunk['supervisor']
                messages = supervisor_data['messages']
                for msg in messages:
                    reasoning = msg.additional_kwargs.get("reasoning_content")
                    if reasoning:
                        # print(f"{reasoning} \n\n")
                        yield json.dumps({
                            "type": "thinking",
                            "content": reasoning
                        }) + "\n"



@router.post("/")
async def chat(request: ChatRequest):
    print(f"chat endpoint hit....Message: {request.message}")
    return StreamingResponse(
        stream_graph_response(request.message),
        media_type="text/event-stream"
    )
