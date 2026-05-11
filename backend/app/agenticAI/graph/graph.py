from langgraph.graph import StateGraph,END,START
from app.agenticAI.schema.schema import AgentState
from app.agenticAI.Nodes.nodes import extract_intent,search_node,compare_node,recommend_node,synthesize_response,route_intent,general_node


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("extract_intent",extract_intent)
    graph.add_node("search",search_node)
    graph.add_node("compare",compare_node)
    graph.add_node("recommend",recommend_node)
    graph.add_node("synthesize", synthesize_response)
    graph.add_node("general",general_node)


    graph.add_edge(START,"extract_intent")
    graph.add_conditional_edges(
        "extract_intent",
        route_intent,
        {
            "search":"search",
            "compare":"compare",
            "recommend":"recommend",
            "general":"general"
        }
    )
    
    graph.add_edge("search","synthesize")
    graph.add_edge("compare","synthesize")
    graph.add_edge("recommend","synthesize")
    graph.add_edge("general","synthesize")

    graph.add_edge("synthesize",END)

    return graph.compile()

app = build_graph()

# res = app.invoke({"user_query": "Search for a SSD"})

# print(res['final_response'])