from typing import Annotated,TypedDict,Literal,Any
from langgraph.graph.message import add_messages
from pydantic import BaseModel,Field

class UserIntent(BaseModel):
    """Structured representation of parsed user intent"""

    intent_type: Literal['search','compare','recommend','general'] = Field(...,description="The classified intent category")
    query: str = Field(...,description="The user query")
    entities: dict[str,Any] = Field(default_factory=dict,description ="Extracted entities: category, min_price, max_price, product_ids, product_name, keywords")


class AgentState(TypedDict):
    """Shared state flowing through the langgraph workflow."""

    messages: Annotated[list, add_messages]
    user_query: str
    intent: UserIntent | None
    products: list[dict]
    agent_output: str
    final_response: str
    reasoning: str

class ProductRating(BaseModel):
    """Product rating according to FakeStoreAPI."""

    rate: float = Field(...,description = "Average rating (0-5)")
    count: int = Field(...,description = "Number of ratings")

class Product(BaseModel):
    """A single product from FakeStoreAPI."""
    id: int
    title: str
    price: float
    description: str
    category: str
    image: str
    rating: ProductRating