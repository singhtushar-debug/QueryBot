from fastapi import APIRouter
from app.api.routes import ingest, query, chat

api_router = APIRouter()

api_router.include_router(ingest.router, prefix="/ingest")
api_router.include_router(query.router, prefix="/query")
api_router.include_router(chat.router, prefix="/chat")
