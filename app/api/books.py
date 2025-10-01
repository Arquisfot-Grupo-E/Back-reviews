import logging
from fastapi import APIRouter, HTTPException, Query
from app.services.google_books import search_books, get_book_by_id
from app.schemas.book import Book

router = APIRouter()

@router.get("/search", response_model=list[Book])
async def search_books_endpoint(q: str = Query(..., description="Texto para buscar en Google Books")):
    try:
        results = await search_books(q, max_results=10)  # 👈 await + async
        if not results:
            raise HTTPException(status_code=404, detail="No se encontraron libros")
        return results
    except Exception as e:
        logging.error(f"Error searching books for query '{q}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/id/{book_id}", response_model=Book)
async def get_book(book_id: str):
    try:
        book = await get_book_by_id(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        return book
    except Exception as e:
        logging.error(f"Error fetching book with id '{book_id}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    
@router.get("/review/search", response_model=list[Book])
async def search_books_review_endpoint(q: str = Query(..., description="Texto para buscar en Google Books")):
    try:
        results = await search_books(q, max_results=10)  # 👈 await + async
        if not results:
            raise HTTPException(status_code=404, detail="No se encontraron libros")
        return results
    except Exception as e:
        logging.error(f"Error searching books for query '{q}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")