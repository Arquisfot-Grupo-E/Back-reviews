from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import books

app = FastAPI(title="Book Search API")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(books.router, prefix="/books", tags=["books"])

@app.get("/")
def root():
    return {"message": "Book Search API is running"}
