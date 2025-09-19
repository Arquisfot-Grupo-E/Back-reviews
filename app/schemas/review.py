from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ReviewCreate(BaseModel):
    google_book_id: str
    content: str

class ReviewOut(BaseModel):
    id: int
    user_id: UUID
    google_book_id: str
    content: str
    karma_score: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReviewUpdate(BaseModel):
    content: str

class KarmaVoteInput(BaseModel):
    value: int  # +1 o -1
