from fastapi import APIRouter, HTTPException, Query
from app.services.google_books import search_books
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
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
