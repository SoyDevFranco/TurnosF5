# routers/users_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from crud.user_crud import create_user, get_user, update_user, delete_user
from schemas.users import UserBase, UserUpdate

# Se crea una instancia de APIRouter para manejar las rutas
router = APIRouter()


# Ruta para crear un nuevo usuario
@router.post("/users/", response_model=UserBase)
def create_new_user(user: UserBase, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


# Ruta para obtener un usuario por su ID
@router.get("/users/{user_id}", response_model=UserBase)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        # Lanza un error si el usuario no se encuentra
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user


# Ruta para actualizar un usuario existente
@router.put("/users/{user_id}", response_model=UserBase)
def update_existing_user(
    user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)
):
    updated_user = update_user(db, user_id, user_update)
    if updated_user is None:
        # Lanza un error si el usuario no se encuentra
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated_user


# Ruta para eliminar un usuario por su ID
@router.delete("/users/{user_id}", response_model=UserBase)
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = delete_user(db, user_id)
    if deleted_user is None:
        # Lanza un error si el usuario no se encuentra
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return deleted_user
