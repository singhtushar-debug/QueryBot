from langchain_core.runnables  import RunnableParallel,RunnablePassthrough,RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from app.rag.prompts import prompt
from app.llm.huggingface import get_llm
from app.rag.retriever import get_retriever
from app.vectorstore.chroma import get_vectorstore


llm = get_llm()
vectorstore = get_vectorstore()
retriever = get_retriever(vectorstore)
parser = StrOutputParser()


def format_docs(retrieved_docs):
    context = " ".join(doc.page_content for doc in retrieved_docs)
    return context


parallel_chain = RunnableParallel({
    'context': retriever | RunnableLambda(format_docs),
    'question': RunnablePassthrough()
})


main_chain = parallel_chain | prompt | llm | parser

def get_chain():
    return main_chain