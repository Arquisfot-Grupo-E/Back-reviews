from pydantic import BaseModel
from typing import List, Optional

class Book(BaseModel):
    id: str
    title: str
    authors: Optional[List[str]] = None
    publisher: Optional[str] = None
    published_date: Optional[str] = None
    description: Optional[str] = None
    thumbnail: Optional[str] = None

