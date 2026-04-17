from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('HUGGINGFACEHUB_API_KEY')

def get_vectorstore():
    embedding_model = HuggingFaceEndpointEmbeddings(model = 'sentence-transformers/all-MiniLM-L6-v2',task = 'feature-extraction',huggingfacehub_api_token = api_key)

    vectordb = Chroma(
        embedding_function= embedding_model
    )
    return vectordb