# auth/dependencies.py
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.users import User
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

# Configuración de JWT
JWT_SECRET_KEY = "my_jwt_secret_key"  # Cambiar por una clave secreta segura
JWT_ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Endpoint para obtener el token


def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload.get("sub")  # Asume que "sub" es el email o ID del usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido.")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    email = decode_jwt(token)

    if email is None:
        raise HTTPException(status_code=401, detail="No se pudo validar el usuario.")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    return user
