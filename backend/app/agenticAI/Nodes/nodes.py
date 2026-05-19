from langchain_core.messages import SystemMessage
from langgraph.prebuilt import InjectedState
from typing import Annotated
from langchain_core.tools import tool
from app.llm.huggingface import get_llm
from app.agenticAI.schema.schema import AgentState
from app.agenticAI.agents.agents import product_agent, general_agent, cart_agent


# wrapping specialized sub-agents as a tool
@tool
async def product_agent_tool(query:str,state: Annotated[dict, InjectedState]):
    """
        Handle product related queries.

        Args:
            query: original user query (must be a string).
    """
    print("product agent working...")

    response = await product_agent.ainvoke({
        "query": query,
        "messages": state["messages"]
        })

    return response["messages"][-1].content


@tool
async def cart_agent_tool(query: str,state: Annotated[dict,InjectedState],product_id: int | None = None,quantity: int = 1):
    """
        Handle user cart related queries.

        Args:
            query: original user query (must be a string).
            product_id: product id (must be an integer).
            quantity: quantity to add (must be an integer).
    """
    print("cart agent working....")

    response = await cart_agent.ainvoke({
        "query": query,
        "product_id": product_id,
        "quantity": quantity,
        "messages": state['messages']
        })

    return response["messages"][-1].content


@tool
async def general_agent_tool(query: str,state: Annotated[dict, InjectedState]):
    """
        Handle general chat.

        Args:
            query: original user query (must be a string).
    """
    print("general agent working...")
    response = await general_agent.ainvoke({
        "query": query,
        "messages": state["messages"]
        })
    
    return response["messages"][-1].content


system_prompt = """
        You are the supervisor for QueryBot.\n
        Your job is to solve the user's request by calling the appropriate specialized tools.

        Available tools:\n
        - product_agent_tool: Call this tool for product related query (search,recommend,compare). \n
        - cart_agent_tool: Call this tool for adding/removing items from the cart or viewing the cart. \n
        - general_agent_tool: Call this tool for general greetings or questions. \n
        
        GUIDELINES:
        1.Important: Always extract product_ids of each product  (that is used to pass to other agents)
        2.Important: Don't answer from the conversational history alone,call the appropriate tools see the tools response and then provide the final reponse.
    """
supervisor_tools = [product_agent_tool, general_agent_tool, cart_agent_tool]


async def supervisor_node(state: AgentState):
    llm = get_llm()

    messages = [SystemMessage(content=system_prompt)] + state["messages"]

    llm_with_tools = llm.bind_tools(supervisor_tools)

    print("supervisor node working...")
    response = await llm_with_tools.ainvoke(messages)
    
    return {"messages": [response], "final_response": f"from supervisor: {response.content}"}
