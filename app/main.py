from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.books import router as books_router
from app.api.reviews import router as reviews_router
from app.db.base import Base
from app.db.session import engine
from app.models.review import Review, KarmaVote  

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
app.include_router(books_router, prefix="/books", tags=["books"])
app.include_router(reviews_router, prefix="/reviews", tags=["reviews"])


# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Book Search API is running"}
