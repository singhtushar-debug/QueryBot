from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template = """
        You are a helpful assistant.
        Answer ONLY from the provided context.
        If the context is insufficient , just say you don't know.

        Context:{context}
        Quesiton:{question}
    """,
    input_variables=['context','question']
)