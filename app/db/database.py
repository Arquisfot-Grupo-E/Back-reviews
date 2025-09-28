# ========================
# ARCHIVO NUEVO/REESCRITO
# ========================
from pymongo import MongoClient
from app.core.config import settings
from bson.codec_options import CodecOptions # <-- AÑADIR esta importación
from uuid import UUID # <-- AÑADIR esta importación

client = MongoClient(settings.MONGODB_URL, uuidRepresentation='standard')
database = client[settings.MONGO_DB_NAME]

# La colección de reseñas
review_collection = database.get_collection("reviews")

# Función para inyectar la colección en las rutas
def get_review_collection():
    return review_collection