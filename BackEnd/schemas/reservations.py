# schemas/reservations.py
from pydantic import BaseModel
from datetime import datetime
from typing import List


class ReservationBase(BaseModel):
    reservation_hours: datetime


class ReservationRequest(BaseModel):
    reservations: List[ReservationBase]
    payment_type: str
