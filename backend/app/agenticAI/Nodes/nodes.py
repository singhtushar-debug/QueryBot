from langchain_core.messages import SystemMessage
from langgraph.prebuilt import InjectedState
from typing import Annotated
from langchain_core.tools import tool
from app.llm.huggingface import get_llm
from app.agenticAI.schema.schema import AgentState
from app.agenticAI.agents.agents import product_agent, general_agent, cart_agent


# wrapping specialized sub-agents as a tool
@tool
def product_agent_tool(state: Annotated[dict, InjectedState]):
    """Handle product related queries."""
    print("product agent working...")

    response = product_agent.invoke({"messages": state["messages"]})

    return response["messages"][-1].content


@tool
def cart_agent_tool(state: Annotated[dict, InjectedState]):
    """Handle user cart related queries."""
    print("cart agent working....")

    response = cart_agent.invoke({"messages": state["messages"]})

    return response["messages"][-1].content


@tool
def general_agent_tool(state: Annotated[dict, InjectedState]):
    """Handle general chat."""
    response = general_agent.invoke({"messages": state["messages"]})
    print("general")
    return response["messages"][-1].content


system_prompt = """
        You are the supervisor for QueryBot.\n
        Your job is to solve the user's request by calling the appropriate specialized tools.

        Available tools:\n
        - product_agent_tool: Call this tool for product related query (search,recommend,compare). \n
        - cart_agent_tool: Call this tool for adding/removing items from the cart or viewing the cart. \n
        - general_agent_tool: Call this tool for general greetings or questions. \n
        
        GUIDELINES:
        Don't answer from the conversational history alone,call the appropriate tools see the tools response and then provide the final reponse.
        
        Final Response:
        - Once you think the user's query can be satisfied by the data provided by the tools.
         Generate a conversational response for the user.


    """
supervisor_tools = [product_agent_tool, general_agent_tool, cart_agent_tool]


def supervisor_node(state: AgentState):
    llm = get_llm()

    messages = [SystemMessage(content=system_prompt)] + state["messages"]

    llm_with_tools = llm.bind_tools(supervisor_tools)

    response = llm_with_tools.invoke(messages)
    print("supervisor node working...")
    return {"messages": [response], "final_response": response.content}

