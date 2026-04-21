from app.vectorstore.chroma import get_vectorstore
from app.rag.chain import get_chain

def get_vs():
    return get_vectorstore()

def get_ch():
    return get_chain()