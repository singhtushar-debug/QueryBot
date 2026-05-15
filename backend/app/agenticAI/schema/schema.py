from typing import Annotated, TypedDict, Optional
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


class AgentState(TypedDict):
    """Shared state flowing through the langgraph workflow."""

    messages: Annotated[list, add_messages]
    user_id: int
    final_response: str


class ProductRating(BaseModel):
    """Product rating according to FakeStoreAPI."""

    rate: float = Field(..., description="Average rating (0-5)")
    count: int = Field(..., description="Number of ratings")


class Product(BaseModel):
    """A single product from FakeStoreAPI."""

    id: int
    title: str
    price: float
    category: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    rating: ProductRating
