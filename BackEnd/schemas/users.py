# schemas/user.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional


# Esquema base con los campos comunes
class UserBase(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    name: Optional[str] = Field(None, example="Juan Perez")
    phone_number: Optional[str] = Field(None, example="+1234567890")


class UserRegister(BaseModel):
    """Esquema para actualizar datos del usuario"""

    name: Optional[str] = Field(None, example="Updated Name")
    phone_number: Optional[str] = Field(None, example="+1234567890")


class UserCreate(UserBase):
    """Esquema para crear un usuario, donde el email es obligatorio"""


class UserUpdate(BaseModel):
    """Esquema para actualizar datos del usuario"""

    name: Optional[str] = Field(None, example="Updated Name")
    phone_number: Optional[str] = Field(None, example="+1234567890")


{"reservation_id": 7}
