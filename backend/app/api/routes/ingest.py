from fastapi import APIRouter,Depends,UploadFile,File
from pydantic import BaseModel
from app.rag.ingestion import ingest_url,ingest_pdf
from app.dependencies import get_vs
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok = True)


class IngestRequest(BaseModel):
    url: str


@router.post("/")
def ingest(data: IngestRequest,vs = Depends(get_vs)):
    ingest_url(data.url,vs)

    return {"message": "Data igested successfully"}

@router.post("/pdf")
def ingest_pdf_endpoint(file: UploadFile = File(...), vs = Depends(get_vs)):
    # print(type(file))
    file_path = os.path.join(UPLOAD_DIR,file.filename)

    with open(file_path, 'wb') as f:
        f.write(file.file.read())

    ingest_pdf(file_path, vs)

    return {"message": "PDF ingested"}