from app.rag.chain import get_chain
from app.rag.ingestion import ingest_url
from app.vectorstore.chroma import get_vectorstore

vectorstore = get_vectorstore()

def query_process(url,query):
    ingest_url(url,vectorstore)

    chain = get_chain()

    response = chain.invoke(query)

    return response


print(query_process(url = 'https://www.geeksforgeeks.org/machine-learning/machine-learning/',query = 'What is  machine learning?'))