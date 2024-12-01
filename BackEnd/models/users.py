# models/users.py
from sqlalchemy import Column, Integer, String, UniqueConstraint
from db.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="uq_user_email"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    name = Column(String(50), nullable=True)
    phone_number = Column(String(20), nullable=True)

    reservations = relationship("Reservation", back_populates="user")
    # Relación con Payments
    payments = relationship("Payment", back_populates="user")
