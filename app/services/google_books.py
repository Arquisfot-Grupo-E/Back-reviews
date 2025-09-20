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
            "id": item.get("id"),  
            "title": volume_info.get("title"),
            "authors": volume_info.get("authors", []),
            "publisher": volume_info.get("publisher"),
            "published_date": volume_info.get("publishedDate"),
            "description": volume_info.get("description"),
            "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail"),
        })

    return books

async def get_book_by_id(book_id: str):
    url = f"{settings.GOOGLE_BOOKS_API_URL}/{book_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            # Aquí puedes mapear `data` a tu schema Book
            return {
                "id": data.get("id"),
                "title": data["volumeInfo"].get("title"),
                "authors": data["volumeInfo"].get("authors", []),
                "published_date": data["volumeInfo"].get("publishedDate"),
                "description": data["volumeInfo"].get("description"),
                "thumbnail": data["volumeInfo"].get("imageLinks", {}).get("thumbnail")
            }
        return None
