from langchain_community.document_loaders import WebBaseLoader,PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def ingest_url(url,vectorstore):
    loader = WebBaseLoader(url)
    docs = loader.load()

    process_docs(docs,vectorstore)
    

def ingest_pdf(file_path,vectorstore):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    # print(docs)
    process_docs(docs,vectorstore)



def process_docs(docs,vectorstore):
    splitter = RecursiveCharacterTextSplitter(chunk_size = 500,chunk_overlap = 50)
    chunks = splitter.split_documents(docs)

    vectorstore.add_documents(chunks)