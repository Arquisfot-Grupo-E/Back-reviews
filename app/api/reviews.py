from fastapi import APIRouter, Depends, HTTPException, Body
from pymongo.collection import Collection
from app.schemas.review import ReviewCreate, ReviewOut, ReviewUpdate, KarmaVoteInput
from app.db.database import get_review_collection
from app.core.security import get_current_user_id
from uuid import UUID
from datetime import datetime
from bson import ObjectId
from pymongo.errors import DuplicateKeyError


router = APIRouter()

# Helper para convertir un documento de MongoDB a un diccionario que Pydantic pueda usar
def document_to_dict(doc):
    if doc and "_id" in doc:
        doc["id"] = str(doc["_id"])
    return doc

@router.post("/", response_model=ReviewOut)
def create_review(
    review: ReviewCreate,
    collection: Collection = Depends(get_review_collection),
    user_id: UUID = Depends(get_current_user_id)
):
    if collection.find_one({"user_id": user_id, "google_book_id": review.google_book_id}):
        raise HTTPException(status_code=400, detail="Ya tienes una reseña para este libro")

    # MODIFICADO: Incluimos el rating
    new_review_data = {
        "user_id": user_id,
        "google_book_id": review.google_book_id,
        "content": review.content,
        "rating": review.rating, # <-- AÑADIDO
        "karma_score": 0,
        "votes": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = collection.insert_one(new_review_data)
    created_review = collection.find_one({"_id": result.inserted_id})
    return document_to_dict(created_review)



@router.get("/my-reviews", response_model=list[ReviewOut])
def get_my_reviews(
    collection: Collection = Depends(get_review_collection),
    user_id: UUID = Depends(get_current_user_id)
):
    reviews_cursor = collection.find({"user_id": user_id}).sort("created_at", -1)
    return [document_to_dict(review) for review in reviews_cursor]


@router.patch("/{id}", response_model=ReviewOut)
def update_review(  # <-- Nombre cambiado para mayor claridad
    id: str,
    update: ReviewUpdate,
    db: Collection = Depends(get_review_collection), # <-- Cambiado nombre a 'db' o 'collection'
    user_id: UUID = Depends(get_current_user_id)
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de reseña inválido")

    review = db.find_one({"_id": ObjectId(id)})
    if not review:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")

    if review["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar esta reseña")

    # Construimos el documento de actualización dinámicamente
    update_data = update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")
    
    update_data["updated_at"] = datetime.utcnow()

    updated_result = db.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": update_data},
        return_document=True
    )
    return document_to_dict(updated_result)



@router.delete("/{id}")
def delete_review(
    id: str,
    collection: Collection = Depends(get_review_collection),
    user_id: UUID = Depends(get_current_user_id)
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de reseña inválido")
        
    review = collection.find_one({"_id": ObjectId(id)})
    if not review:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")

    if review["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta reseña")

    delete_result = collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Reseña no encontrada para eliminar")
        
    return {"detail": "Reseña eliminada correctamente"}


@router.post("/{id}/vote", response_model=ReviewOut)
def vote_review(
    id: str,
    vote: KarmaVoteInput,
    collection: Collection = Depends(get_review_collection),
    user_id: UUID = Depends(get_current_user_id)
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de reseña inválido")
    if vote.value not in [-1, 1]:
        raise HTTPException(status_code=400, detail="El valor del voto debe ser -1 o 1")

    # Primero, quita cualquier voto previo del usuario
    collection.update_one(
        {"_id": ObjectId(id), "votes.voter_id": user_id},
        {"$pull": {"votes": {"voter_id": user_id}}}
    )

    # Luego, agrega el nuevo voto
    result = collection.update_one(
        {"_id": ObjectId(id)},
        {"$push": {"votes": {"voter_id": user_id, "value": vote.value}}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")

    # Recalcula el karma_score (más seguro que usar $inc)
    pipeline = [
        {"$match": {"_id": ObjectId(id)}},
        {"$unwind": "$votes"},
        {"$group": {"_id": "$_id", "total_karma": {"$sum": "$votes.value"}}}
    ]
    karma_result = list(collection.aggregate(pipeline))
    new_karma = karma_result[0]['total_karma'] if karma_result else 0
    
    collection.update_one({"_id": ObjectId(id)}, {"$set": {"karma_score": new_karma}})
    
    # return {"karma_score": new_karma}
    updated_review = collection.find_one({"_id": ObjectId(id)})
    return document_to_dict(updated_review)

@router.get("/users/{user_id}", response_model=list[ReviewOut])
def get_reviews_by_user(
    user_id: UUID,
    collection: Collection = Depends(get_review_collection)
):
    reviews_cursor = collection.find({"user_id": user_id}).sort("created_at", -1)
    return [document_to_dict(review) for review in reviews_cursor]


@router.get("/book/{google_book_id}", response_model=list[ReviewOut])
def get_reviews_for_book(
    google_book_id: str,
    collection: Collection = Depends(get_review_collection)
):
    """
    Obtiene todas las reseñas para un libro específico, ordenadas por fecha de creación descendente.
    """
    reviews_cursor = collection.find(
        {"google_book_id": google_book_id}
    ).sort("created_at", -1)  # -1 para orden descendente (más nuevas primero)

    return [document_to_dict(review) for review in reviews_cursor]