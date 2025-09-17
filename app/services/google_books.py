import httpx
from app.core.config import settings

GOOGLE_BOOKS_API_URL = settings.GOOGLE_BOOKS_API_URL

async def search_books(query: str, max_results: int = 10):
    """
    Consulta la API de Google Books y devuelve una lista con datos limpios.
    """
    params = {
        "q": query,
        "maxResults": max_results
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_BOOKS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

    books = []
    for item in data.get("items", []):
        volume_info = item.get("volumeInfo", {})
        books.append({
            "title": volume_info.get("title"),
            "authors": volume_info.get("authors", []),
            "publisher": volume_info.get("publisher"),
            "published_date": volume_info.get("publishedDate"),
            "description": volume_info.get("description"),
            "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail"),
        })

    return books
