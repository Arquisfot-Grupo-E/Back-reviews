from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewOut
from app.db.session import get_db
from app.core.security import get_current_user_id
from uuid import UUID

router = APIRouter(tags=["Reviews"])

@router.post("/", response_model=ReviewOut)
def create_review(
    
    review: ReviewCreate,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    new_review = Review(**review.dict(), user_id=user_id)
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@router.get("/my-reviews", response_model=list[ReviewOut])
def get_my_reviews(
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    return db.query(Review).filter(Review.user_id == user_id).order_by(Review.created_at.desc()).all()