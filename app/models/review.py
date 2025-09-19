from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID, nullable=False)  # viene del JWT
    google_book_id = Column(String, nullable=False)  # volumeId de Google Books
    content = Column(Text, nullable=False)
    karma_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación con votos
    votes = relationship("KarmaVote", back_populates="review", cascade="all, delete-orphan")


class KarmaVote(Base):
    __tablename__ = "karma_votes"

    id = Column(Integer, primary_key=True)
    review_id = Column(Integer, ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False)
    voter_id = Column(UUID, nullable=False)  # también viene del JWT
    value = Column(Integer, nullable=False)  # +1 o -1

    # Restricción: un usuario solo puede votar una vez por reseña
    __table_args__ = (
        UniqueConstraint("review_id", "voter_id", name="unique_vote_per_user"),
    )

    # Relación inversa
    review = relationship("Review", back_populates="votes")