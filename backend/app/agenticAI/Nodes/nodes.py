from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
# from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from app.llm.huggingface import get_llm
from app.agenticAI.schema.schema import AgentState,UserIntent
from app.agenticAI.tools.tools import compare_products,search_products,fetch_all_products,fetch_product_by_id,rank_products
import json

parser = PydanticOutputParser(pydantic_object=UserIntent)

# def get_llm():
#     """Get LLM"""
    # return ChatGoogleGenerativeAI(model = 'gemini-2.5-flash',google_api_key = os.getenv('GOOGLE_API_KEY'))


INTENT_SYSTEM_PROMPT = ChatPromptTemplate.from_messages([
    ("system" , """\
You are an intent classifier for an e-commerce shopping assistant called ShopWiseAI.

Analyze the user's message and extract:
1. **intent_type**: One of: search, compare, knowledge, cart_add, cart_view, recommend, general
2. **query**: A cleaned version of the user's request
3. **entities**: A JSON object with any of these optional fields:
   - category: product category (electronics (if user ask about any electornics product), jewelery (if user ask for any jewelery related query), men's clothing, women's clothing)
   - min_price: minimum price (number)
   - max_price: maximum price (number)
   - product_ids: list of product IDs mentioned
   - product_name: specific product name mentioned
   - keywords: list of search keywords

Intent definitions:
- **search**: User wants to find/browse products (e.g., "show me laptops", "find cheap shirts")
- **compare**: User wants to compare specific products (e.g., "compare the two SSDs", "which hard drive is better")
- **knowledge**: User wants buying advice or information (e.g., "what should I look for in a monitor", "tell me about SSD types")
- **cart_add**: User wants to add a product to their cart (e.g., "add the jacket to my cart", "I'll take product 3")
- **cart_view**: User wants to see their cart (e.g., "show my cart", "what's in my basket")
- **recommend**: User wants personalized recommendations (e.g., "what do you recommend for a gift", "best bang for the buck")
- **general**: Greetings, thanks, or unrelated queries

Return result strictly in json format and strictly follow the format instructoins :
     
{format_instructions}
     
"""),

("human","{query}")

])


def extract_intent(state: AgentState):
    """Parse user query into structured intent using LLM"""
    user_query = state['user_query']
    llm = get_llm()

    chain = INTENT_SYSTEM_PROMPT | llm | parser

    response = chain.invoke({
        "query":user_query,
        "format_instructions":parser.get_format_instructions()
        })

    print(response)
    # print(type(response))
    return {
        "intent": response,
        "messages":[HumanMessage(content = user_query)]
    }

def route_intent(state: AgentState):
    """"Return the routing key based on extracted intent."""
    intent = state.get('intent')

    return intent.intent_type


def search_node(state: AgentState):
    """Search for products matching the user's criteria."""
    intent = state['intent']
    entities = intent.entities

    products = search_products(
        query = intent.query,
        category = entities.get('category',None),
        min_price = entities.get('min_price',None),
        max_price = entities.get('max_price',None)
    )

    if not products:
        products = fetch_all_products()

    product_dicts = [p.model_dump() for p in products]

    agent_output = json.dumps(
        {
            "action": "search",
            "result_count":len(product_dicts),
            "results":product_dicts,
        }
    )


    return {
        "products": products,
        "agent_output": agent_output,
        "reasoning": (
            f"Found {len(products)} products matching the query."
            f"Applied scoring based on price,rating and popularity."
        )
    }



def compare_node(state: AgentState):
    """Compare products"""
    intent = state['intent']
    entities = intent.entities
    product_ids: list[int] = entities.get("product_ids",[])

    products_to_compare = []

    if product_ids:
        for pid in product_ids:
            product = fetch_product_by_id(pid)
            if product:
                products_to_compare.append(product)
    
    if not products_to_compare:
        search_results = search_products(query = intent.query)
        products_to_compare = search_results

    if not products_to_compare:
        all_products = fetch_all_products()
        products_to_compare = all_products
    
    comparison = compare_products(products_to_compare)

    agent_output = json.dumps(
        {
            "action": "compare",
            "comparison": comparison,
        }
    )

    return {
        "products": products_to_compare,
        "agent_output": agent_output,
        "reasoning":(
            f"Compared {len(products_to_compare)} products using weighted scoring (price:50% , rating: 30% and popularity: 20%)"
            f"Generated recommendation"
        )
    }


def recommend_node(state:AgentState):
    """Generate recommendations."""
    intent = state['intent']
    entities = intent.entities

    products = search_products(
        query = intent.query,
        category = entities.get('category','general'),
        min_price = entities.get('min_price',None),
        max_price = entities.get('max_price',None)
    )

    if not products:
        products = fetch_all_products()

    rank = rank_products(products)

    llm = get_llm()

    products_info = "\n".join(
        f"- {p.title} | ${p.price } | {p.description} | *{p.rating.rate} | {p.rating.count} reviews"
        for p in products
    )

    messages = [
        SystemMessage(
            content = (
                "You are a helpful shopping recommendation assistant.Based on the user's need and the available products data"
                "provide concise, perosnalized recommendation. Explain why you recommend each product.\n"
                f"Available products:\n {products_info}"
                f"Scoring data: \n {json.dumps(rank)}"
            )
        ),
        HumanMessage(content = intent.query),
    ]

    res = llm.invoke(messages)
    # print(res)

    agent_output = json.dumps(
        {
            "action":"recommend",
            "product recommendations":rank,
            "narrative": res.content,
        }
    )

    return {
        "products": products,
        "agent_ouput": agent_output,
        "reasoning": (
            f"Analyzed {len(products)} products.Ranked by weighted score (price 50%, rating 30% and popularity 20% )"
            f"Generated recommendation narrative."
        )
    }


def general_node(state: AgentState):
    """Handle general chat,greetings and unclear queries."""
    intent = state["intent"]
    llm = get_llm()

    messages =  [
        SystemMessage(
            content = (
                "You are a friendly and helpful e-commerce shopping assistant."
                "You help users discover, compare and purchase products."
                "Available categories: electronics, jewelery, men's clothing, women's clothing.\n"
                "If the user greets you, respond warmly and explain what you can do."
                "If their query is unclear, ask for clarification.Always be concise and helpful."
            )
        ),
        HumanMessage(content = intent.query)
    ]

    response = llm.invoke(messages)

    # print(f"general_node : {response}")

    agent_output = json.dumps(
        {
            "action":"general",
            "response": response.content
        }
    )
    return {
        "agent_output": agent_output,
        "reasoning": "Handled as general conversation/greeting"
    }

RESPONSE_SYNTHESIS_PROMPT = """\
You are ShopWiseAI's response synthesizer. Your job is to take the raw agent \
output and create a polished, user-friendly response.

Guidelines:
- Be conversational and helpful
- Dont add products or information about any product from your own knowldege ,provide response solely based on the products infor provided to you.
- If products are involved, highlight key details (name, price, rating)
- If comparisons were made, present them clearly with trade-offs
- If recommendations are given, explain the reasoning
- Keep responses concise but thorough
- Use markdown formatting for readability (bold, bullet points)
- Never expose raw JSON to the user

"""

def synthesize_response(state: AgentState):
    """Conver raw agent output into polished user-facing response."""
    agent_output = state.get("agent_output","")
    reasoning = state.get("reasoning","")
    user_query = state.get("user_query","")

    llm = get_llm()
    print(len(state.get('products',[])))
    messages = [
        SystemMessage(content = RESPONSE_SYNTHESIS_PROMPT),
        HumanMessage(
            content = (
                f"User asked: {user_query} \n\n"
                f"Agent output:\n {agent_output}\n\n"
                f"Available products:\n {state.get('products',[])}"
                f"Reasoning: {reasoning}\n\n"
                f"Create a polished, helpful response for the user."
            )
        )
    ]

    res = llm.invoke(messages)

    return {
        "final_response": res.content,
        "messages": [AIMessage(content = res.content)]
    }