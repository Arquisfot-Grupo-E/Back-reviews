from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.api.books import router as books_router
from app.api.reviews import router as reviews_router
import os
# from app.db.base import Base
# from app.db.session import engine
# from app.models.review import Review, KarmaVote

# ============================================
# THROTTLING CONFIGURATION
# ============================================

# Crear limiter basado en IP del cliente
limiter = Limiter(key_func=get_remote_address)

# Leer configuración desde variables de entorno
ENABLE_THROTTLING = os.getenv("ENABLE_THROTTLING", "true").lower() == "true"

app = FastAPI(
    title="Book Search & Reviews API",
    description="API with Throttling and Rate Limiting",
    version="2.0.0"
)

# Agregar rate limiter a la app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware de SlowAPI (solo si está habilitado)
if ENABLE_THROTTLING:
    app.add_middleware(SlowAPIMiddleware)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:5173"],  # tu frontend
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(books_router, prefix="/books", tags=["books"])
app.include_router(reviews_router, prefix="/reviews", tags=["Reviews"])


# Crear las tablas si no existen
# Base.metadata.create_all(bind=engine)

@app.get("/")
@limiter.limit("100/minute")  # 100 requests por minuto para root
def root(request: Request):
    return {
        "message": "Book Search & Reviews API is running",
        "version": "2.0.0",
        "throttling_enabled": ENABLE_THROTTLING
    }


@app.get("/health")
def health_check():
    """Health check endpoint sin rate limiting"""
    return {
        "status": "healthy",
        "service": "reviews-api"
    }
