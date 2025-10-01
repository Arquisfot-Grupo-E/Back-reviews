# Back-reviews

# Crear el archivo .env a partir del ejemplo
cp .env.example .env

# docker 
docker-compose up --build


# Explicacion Flujo de reviews




Este repositorio se encarga de hacer el CRUD de las reseñas, ademas de usar la API de Google Books para encontrar libros segun su titulo y segun su id

1. Creación de una reseña
	 - El usuario envía una petición POST a `/reviews/` con los datos de la reseña (por ejemplo: `google_book_id`, `title`, `content`, `rating`,`votes`).
	 - El backend comprueba que el usuario (identificado por `user_id` en el token o en el stub de seguridad) no haya creado ya una reseña para ese `google_book_id`.
	 - Si ya existe una reseña del mismo usuario para ese libro, se devuelve un error (se impone una reseña por usuario por libro).
	 - Si no existe, se inserta un documento en la colección `reviews` en MongoDB y se devuelve la reseña creada.

2. Lectura de reseñas
	 - `GET /reviews/book/{google_book_id}` devuelve todas las reseñas para un libro dado.
	 - `GET /reviews/my-reviews` devuelve las reseñas asociadas al usuario actual (en el entorno de desarrollo el `user_id` puede venir de `app/core/security.py`).

3. Actualización y borrado
	 - `PATCH /reviews/{id}` permite al autor (owner) actualizar su reseña.
	 - `DELETE /reviews/{id}` permite al autor eliminar su reseña.
	 - El backend valida que el `user_id` del request coincida con el `user_id` almacenado en la reseña antes de permitir la operación.

4. Votación (karma)
	 - `POST /reviews/{id}/vote` admite votos positivos o negativos.
	 - El usuario puede votar una reseña; el endpoint gestiona la lógica para añadir o actualizar la entrada de voto y actualizar el contador total de karma en la reseña.
	 - La colección puede tener un subdocumento o colección relacionada para almacenar quién ha votado y evitar votos duplicados por usuario.

5. Consistencia y errores comunes
	 - En caso de conflicto (por ejemplo, intento de crear una segunda reseña por el mismo usuario para el mismo libro) se devuelve 400/409 con un mensaje claro.
	 - Si MongoDB no está disponible, los endpoints retornan errores 5xx; revisar `MONGODB_URL` y la conectividad.

## Organización del proyecto

Breve descripción de las carpetas y archivos más importantes (manteniendo el contenido original del README arriba):

- `app/main.py`
	- Punto de entrada FastAPI. Registra routers (por ejemplo `/books`, `/reviews`) y middleware (CORS).

- `app/api/books.py`
	- Endpoints que consumen la API de Google Books (búsqueda por texto, obtener por id).

- `app/api/reviews.py`
	- Rutas CRUD y lógica de votación para reseñas. Usa la colección `reviews` de MongoDB mediante la dependencia `get_review_collection()`.

- `app/services/google_books.py`
	- Cliente/ayudantes para llamar a Google Books (funciones `search_books`, `get_book_by_id`).

- `app/db/database.py`
	- Inicializa `MongoClient` usando `settings.MONGODB_URL` y obtiene `review_collection`. Exporta `get_review_collection()` para inyectar la colección en los handlers.

- `app/core/config.py`
	- Carga variables de entorno con pydantic-settings (revisa `MONGODB_URL`, `MONGO_DB_NAME`, `GOOGLE_BOOKS_API_URL`).

- `app/core/security.py`
	- Helpers de seguridad y autenticación. Actualmente puede contener un stub que retorna un `user_id` de prueba en desarrollo.

- `requirements.txt`
	- Lista de dependencias (FastAPI, uvicorn, pymongo, httpx, pydantic-settings, etc.).




