# models/payment.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    payment_id = Column(String(50), unique=True, nullable=False)
    amount_paid = Column(Float, nullable=False)

    user = relationship("User", back_populates="payments")
    reservation = relationship("Reservation", back_populates="payment", uselist=False)
