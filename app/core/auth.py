
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings

# Estas variables deben estar en tu .env
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # tokenUrl es un placeholder

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception