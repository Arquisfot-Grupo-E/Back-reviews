from fastapi import FastAPI
from app.api import books

app = FastAPI(title="Book Search API")

# Registrar rutas
app.include_router(books.router, prefix="/books", tags=["books"])

@app.get("/")
def root():
    return {"message": "Book Search API is running"}
