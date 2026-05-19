# from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

def get_llm():
    llm = ChatGroq(groq_api_key=api_key, model="qwen/qwen3-32b",streaming=True)
    return llm



# api_key = os.getenv('HUGGINGFACEHUB_API_KEY')

# def get_llm():
#     model = HuggingFaceEndpoint(
#         repo_id= 'Qwen/Qwen3-32B',
#         task = 'text-generation',
#         huggingfacehub_api_token=api_key,
#         max_new_tokens = 32768
#     )

#     llm = ChatHuggingFace(llm = model)
#     return llm

