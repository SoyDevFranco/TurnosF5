# routers/google_auth_router.py
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.users import UserCreate, UserUpdate
from auth.auth_base import verify_google_token, create_access_token
from crud.user_crud import create_user, update_user as update_user_service
from models.users import User
from pydantic import BaseModel
from auth.dependencies import get_current_user

router = APIRouter()


class GoogleAuthRequest(BaseModel):
    token: str


@router.post("/google")  # http://localhost:8001/auth/google"
async def google_auth(auth_request: GoogleAuthRequest, db: Session = Depends(get_db)):
    token = auth_request.token
    print(f"Token recibido: {token}, pepe: {auth_request.pepe}")

    try:
        payload = verify_google_token(token)
        email = payload.get("email")
        print(f"Email obtenido del token: {email}")
    except HTTPException as e:
        print(f"Error al verificar el token: {e.detail}")
        raise e

    if email is None:
        print("No se encontró un email en el token de Google")
        raise HTTPException(status_code=400, detail="No email found in Google token")

    # Buscar usuario en la base de datos
    user = db.query(User).filter(User.email == email).first()
    print(f"Usuario encontrado: {user}")

    if user is None:
        # Crear un nuevo usuario si no existe
        user_data = UserCreate(email=email, name=payload.get("name", "User"))
        print(f"Creando nuevo usuario: {user_data}")
        user = create_user(db, user_data)
        print("Nuevo usuario creado.")

    # Generar el token de acceso
    access_token = create_access_token(data={"sub": user.email})
    print(f"Token de acceso generado: {access_token}")

    return {"access_token": access_token, "user_id": user.id}


# Endpoint para actualizar el usuario con nombre de usuario y teléfono
@router.put("/update_user", status_code=status.HTTP_200_OK)
async def update_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verificar si el usuario autenticado existe en la base de datos
    user = update_user_service(db, current_user.id, user_update)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    return {"detail": "User updated successfully", "user": user}
