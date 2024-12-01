# models/reservations.py
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from db.database import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    payment_id = Column(String(50), ForeignKey("payments.payment_id"), nullable=True)
    reserved_times = Column(String(100), nullable=False)

    user = relationship("User", back_populates="reservations")
    payment = relationship("Payment", back_populates="reservation", uselist=False)
