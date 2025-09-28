from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Any # <-- AÑADIR Any
from bson import ObjectId
from pydantic_core import core_schema # <-- AÑADIR esta importación

# Helper para manejar el ObjectId de MongoDB
class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *args, **kwargs):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

    # 👇 AÑADE ESTE MÉTODO COMPLETO 👇
    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: Any
    ) -> dict[str, Any]:
        """
        Define cómo se representa este tipo en el JSON Schema de OpenAPI.
        Le decimos que se comporte como un string.
        """
        return {"type": "string"}

class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda dt: dt.isoformat(),
            PyObjectId: str,
        }
        populate_by_name = True
class ReviewCreate(BaseModel):
    google_book_id: str
    content: str
    rating: int = Field(..., ge=1, le=5) # <-- AÑADIDO: ge=greater or equal, le=less or equal

class Vote(BaseModel):
    voter_id: UUID
    value: int
class ReviewOut(MongoBaseModel):
    # id: int
    user_id: UUID
    google_book_id: str
    content: str
    rating: int  # <-- AÑADIDO
    karma_score: int
    votes: List[Vote] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReviewUpdate(BaseModel):
    content: str
    rating: Optional[int] = Field(None, ge=1, le=5) # <-- AÑADIDO: Opcional, pero si se provee, debe ser válido

class KarmaVoteInput(BaseModel):
    value: int  # -1, 0, 1

