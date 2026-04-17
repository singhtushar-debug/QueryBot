from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def ingest_url(url,vectorstore):
    loader = WebBaseLoader(url)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size = 500,chunk_overlap = 100)
    chunks = splitter.split_documents(docs)

    vectorstore.add_documents(chunks)