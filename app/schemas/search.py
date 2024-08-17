# app/schemas/search.py
from pydantic import BaseModel, Field

class SearchQuery(BaseModel):
    text: str = Field(..., description="The text to search for")
    k: int = Field(default=5, ge=1, description="The number of results to return")