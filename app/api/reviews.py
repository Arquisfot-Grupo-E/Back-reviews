from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.review import Review, KarmaVote
from app.schemas.review import ReviewCreate, ReviewOut, ReviewUpdate, KarmaVoteInput
from app.db.session import get_db
from app.core.security import get_current_user_id
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=ReviewOut)
def create_review(
    
    review: ReviewCreate,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    # Verificar si ya existe una reseña para este usuario y libro
    existing_review = db.query(Review).filter(
        Review.user_id == user_id,
        Review.google_book_id == review.google_book_id
    ).first()
    if existing_review:
        raise HTTPException(status_code=400, detail="Ya tienes una reseña para este libro")
    
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


@router.patch("/{id}", response_model=ReviewOut)
def update_review_content(
    id: int,
    update: ReviewUpdate,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    review = db.query(Review).filter(Review.id == id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")

    if review.user_id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar esta reseña")

    review.content = update.content
    db.commit()
    db.refresh(review)
    return review


@router.delete("/{id}")
def delete_review(
    id: int,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    review = db.query(Review).filter(Review.id == id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")

    if review.user_id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta reseña")

    db.delete(review)
    db.commit()
    return {"detail": "Reseña eliminada correctamente"}


@router.post("/{id}/vote")
def vote_review(
    id: int,
    vote: KarmaVoteInput,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    review = db.query(Review).filter(Review.id == id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")

    existing_vote = db.query(KarmaVote).filter(
        KarmaVote.review_id == id,
        KarmaVote.voter_id == user_id
    ).first()

    if existing_vote:
        raise HTTPException(status_code=400, detail="Ya votaste esta reseña")

    new_vote = KarmaVote(review_id=id, voter_id=user_id, value=vote.value)
    review.karma_score += vote.value

    db.add(new_vote)
    db.commit()
    db.refresh(review)
    return {"karma_score": review.karma_score}



@router.get("/users/{user_id}", response_model=list[ReviewOut])
def get_reviews_by_user(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    return db.query(Review).filter(Review.user_id == user_id).order_by(Review.created_at.desc()).all()
