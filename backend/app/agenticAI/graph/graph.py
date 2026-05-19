from langgraph.graph import StateGraph, END, START
from app.agenticAI.schema.schema import AgentState
from langgraph.prebuilt import ToolNode
from app.agenticAI.nodes.nodes import supervisor_node, supervisor_tools
from langgraph.checkpoint.memory import InMemorySaver
# import asyncio

checkpointer = InMemorySaver()


def should_continue(state: AgentState):
    """Determine if the agent should continue to tools or finish."""
    messages = state["messages"]
    last_message = messages[-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "supervisor_tools"

    print("no tool call")
    return END


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("supervisor_tools", ToolNode(supervisor_tools))

    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges(
        "supervisor",
        should_continue,
        {"supervisor_tools": "supervisor_tools", END: END},
    )
    graph.add_edge("supervisor_tools", "supervisor")
    return graph.compile(checkpointer=checkpointer)


app = build_graph()


