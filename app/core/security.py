from uuid import UUID
from fastapi import Depends, HTTPException
from app.core.auth import get_current_user

def get_current_user_id(user: dict = Depends(get_current_user)) -> UUID:
    """
    Extrae el user_id del payload del JWT y lo convierte a UUID.
    """
    user_id_from_token = user.get("user_id") 
    
    if user_id_from_token is None:
        raise HTTPException(
            status_code=401, 
            detail="Token inválido: user_id no encontrado en el payload"
        )
    
    try:
        # Se mantiene la conversión de int a UUID para compatibilidad
        # con el servicio de usuarios que emite un ID numérico.
        user_id_int = int(user_id_from_token)
        # Este formato asume que los IDs de usuario de Django son enteros
        # y los convierte a un formato UUID "reservado".
        uuid_string = f"00000000-0000-0000-0000-{user_id_int:012d}"
        return UUID(uuid_string)
    except (ValueError, TypeError) as e:
        raise HTTPException(
            status_code=401, 
            detail=f"Token inválido: no se pudo convertir user_id ('{user_id_from_token}') a UUID: {e}"
        )