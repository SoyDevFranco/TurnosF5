# controllers/saveData.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.reservations import Reservation
from models.payment import Payment
from fastapi import HTTPException
from controllers.utils import validate_reservations


class Save:
    def __init__(
        self,
        db: Session,
        user_id: int,
        payment_id: str,
        amount_paid: int,
        reservations_list: list[str],
    ):
        """
        Clase para gestionar reservas y pagos.
        """
        self.db = db
        self.user_id = user_id
        self.payment_id = payment_id
        self.amount_paid = amount_paid
        self.reservations_list = reservations_list

    def save_payment(self) -> Payment:
        """
        Guarda un nuevo registro de pago en la base de datos.
        """
        try:
            payment_record = Payment(
                payment_id=self.payment_id,
                user_id=self.user_id,
                amount_paid=self.amount_paid,
            )
            self.db.add(payment_record)

            return payment_record
        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Error al guardar el pago: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al guardar el pago")

    def save_reservation(self) -> list[Reservation]:
        """
        Guarda múltiples registros de reserva en la base de datos.
        """
        validate_reservations(self.db, self.reservations_list)
        reservations = []
        for reservation_hours in self.reservations_list:
            try:
                new_reservation = Reservation(
                    user_id=self.user_id,
                    payment_id=self.payment_id,
                    reserved_times=reservation_hours,
                )
                self.db.add(new_reservation)
                reservations.append(new_reservation)
            except SQLAlchemyError as e:
                self.db.rollback()
                print(f"Error al guardar la reserva: {str(e)}")
                raise HTTPException(
                    status_code=500, detail="Error al guardar la reserva"
                )
        return reservations

    def all_save(self):
        """
        Guarda el pago y las reservas en la base de datos de forma atómica.
        """
        try:
            # Iniciar la transacción
            self.db.begin()

            # Guardar el pago
            payment_record = self.save_payment()

            # Guardar las reservas
            reservations = self.save_reservation()

            # Confirmar transacción
            self.db.commit()

            # Refrescar las instancias de los registros guardados
            self.db.refresh(payment_record)
            for reservation in reservations:
                self.db.refresh(reservation)

            print(f"Pago y reservas guardados exitosamente")
            return {"payment": payment_record, "reservations": reservations}

        except Exception as e:
            # Si ocurre un error, realizar rollback de toda la transacción
            self.db.rollback()
            print(f"Error al guardar los datos: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al guardar los datos")
