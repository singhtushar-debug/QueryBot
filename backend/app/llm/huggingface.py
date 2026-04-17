from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('HUGGINGFACEHUB_API_KEY')

def get_llm():
    model = HuggingFaceEndpoint(
        repo_id= 'meta-llama/Llama-3.1-8B-Instruct',
        task = 'text-generation',
        huggingfacehub_api_token=api_key
    )

    llm = ChatHuggingFace(llm = model)
    return llm