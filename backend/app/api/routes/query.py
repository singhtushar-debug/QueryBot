from fastapi import APIRouter,Depends
from pydantic import BaseModel
from app.dependencies import get_ch

router = APIRouter()

class QueryRequest(BaseModel):
    question: str


@router.post("/")
def query(data: QueryRequest,chain = Depends(get_ch)):
    response = chain.invoke(data.question)

    return {"answer": response}