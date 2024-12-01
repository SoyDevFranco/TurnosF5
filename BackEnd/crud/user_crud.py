# crud/user_service.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.users import User
from schemas.users import UserBase, UserUpdate


# Función para crear un nuevo usuario
def create_user(db: Session, user: UserBase):
    try:
        db_user = User(**user.dict())  # Crea una instancia de User con los datos
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()  # Revierte la transacción en caso de error
        raise HTTPException(status_code=500, detail="Error al crear el usuario.") from e


# Función para obtener un usuario por su ID
def get_user(db: Session, user_id: int):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        return user
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail="Error al obtener el usuario."
        ) from e


# Función para actualizar un usuario existente
def update_user(db: Session, user_id: int, user_update: UserUpdate):
    try:
        db_user = get_user(
            db, user_id
        )  # Lanza una excepción si no encuentra el usuario
        # Actualiza atributos del usuario dinámicamente
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()  # Revierte la transacción en caso de error
        raise HTTPException(
            status_code=500, detail="Error al actualizar el usuario."
        ) from e


# Función para eliminar un usuario por su ID
def delete_user(db: Session, user_id: int):
    try:
        db_user = get_user(
            db, user_id
        )  # Lanza una excepción si no encuentra el usuario
        db.delete(db_user)
        db.commit()
        return {"message": "Usuario eliminado correctamente."}
    except SQLAlchemyError as e:
        db.rollback()  # Revierte la transacción en caso de error
        raise HTTPException(
            status_code=500, detail="Error al eliminar el usuario."
        ) from e
