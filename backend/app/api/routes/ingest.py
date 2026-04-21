from fastapi import APIRouter,Depends
from pydantic import BaseModel
from app.rag.ingestion import ingest_url
from app.dependencies import get_vs

router = APIRouter()

class IngestRequest(BaseModel):
    url: str


@router.post("/")
def ingest(data: IngestRequest,vs = Depends(get_vs)):
    ingest_url(data.url,vs)

    return {"message": "Data igested successfully"}