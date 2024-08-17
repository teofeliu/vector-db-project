# app/schemas/search.py
from pydantic import BaseModel, Field
from typing import Optional

class SearchQuery(BaseModel):
    text: str
    k: Optional[int]