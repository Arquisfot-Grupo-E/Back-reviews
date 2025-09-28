from uuid import UUID
from fastapi import Depends, HTTPException
from app.core.auth import get_current_user

#def get_current_user_id() -> UUID:
    #"""
    #Función de prueba: retorna un UUID fijo para simular usuario autenticado.
    #Reemplaza con lógica real de JWT cuando esté listo.
    #"""
    #return UUID("11111111-1111-1111-1111-111111111111")

def get_current_user_id(user: dict = Depends(get_current_user)) -> UUID:
    """
    Extrae y retorna el user_id del payload del JWT.
    """
    user_id = user.get("user_id") 
    
    if user_id is None:
        raise HTTPException(
            status_code=401, 
            detail="Token inválido: user_id no encontrado"
        )
    
    try:
        # Convertir el integer del JWT a UUID usando padding con ceros
        user_id_int = int(user_id)
        uuid_string = f"00000000-0000-0000-0000-{user_id_int:012d}"
        return UUID(uuid_string)
    except (ValueError, TypeError) as e:
        raise HTTPException(
            status_code=401, 
            detail=f"Token inválido: no se pudo convertir user_id a UUID: {str(e)}"
        )
    