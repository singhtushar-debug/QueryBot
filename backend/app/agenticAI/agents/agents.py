from langchain.agents import create_agent
from app.agenticAI.tools.tools import (
    search_products,
    rank_products,
    fetch_categories,
    add_to_cart,
    remove_from_cart,
    view_cart,
    update_quantity,
    clear_cart,
)
from app.llm.huggingface import get_llm


product_agent = create_agent(
    model=get_llm(),
    tools=[search_products, fetch_categories, rank_products],
    system_prompt="""
        You are a specialized product agent for QueryBot.
        Your primary goal is to handle product related queries using the specialized tools.

        AVAILABLE TOOLS:
        1. search_products : Use this tool to search for products.\n
        2. fetch_categories: Use this tool to fetch available categories.\n
        3. rank_products: Use this tool to rank products on the basis of price, rating, review count.\n

        GUIDELINES:
        1. Available categories: electronics, jewelery, men's clothing, women's clothing.
        2. ONLY return structured output of the tools.
        3. If you aren't sure about a category, use fetch_categories first.
        4. IMPORTANT: Do not explain your steps. Call the tool immediately.
        5. IMPORTANT: Do not try to be conversational.Return the structured tool result.
        6. IMPORTANT: Include product_id in your response for each product.
        
    """,
)

cart_agent = create_agent(
    model=get_llm(),
    tools=[add_to_cart, remove_from_cart, view_cart, update_quantity, clear_cart],
    system_prompt="""
        You are a specialized cart agent for QueryBot.
        Your primary goal is to handle cart related queries using the specialized tools.

        AVAILABLE TOOLS:
        1. add_to_cart : Use this tool to add a product in the user cart.\n
        2. remove_from_cart: Use this tool to remove a product from the user cart.\n
        3. view_cart: Use this tool to view all the items in the user cart.\n
        4. update_quantity: Use this tool to update the quantity of a product in the user cart.\n
        5. clear_cart: Use this tool to remove all the products from the user cart.\n

        GUIDELINES:
        1. IMPORTANT: Do not explain your steps. Call the tool immediately.
        2. IMPORTANT: ONLY Return structured tool output.
        3. IMPORTANT: Must include product_id in your response for each product.
        3. Do not give conversational response.
    """,
)


general_agent = create_agent(
    model=get_llm(),
    tools=[],
    system_prompt="""
        You are a helpful assistant for QueryBot and e-commerce shopping assistant.\n
        Greet the user and answer general questions nicely.
    """,
)


# for chunk in product_agent.stream(
#     {"messages": [{"role": "user", "content": "List all the products in the electronics category"}]},
#     stream_mode="updates",
#     version="v2",
# ):
#     if chunk["type"] == "updates":
#         for step, data in chunk["data"].items():
#             print(f"step: {step}")
#             print(f"content: {data['messages'][-1].content_blocks}")
