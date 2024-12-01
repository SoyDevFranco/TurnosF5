# controllers/utils.py
from datetime import datetime
from typing import List
import mercadopago
import os
import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.reservations import Reservation

# Cargar variables de entorno
load_dotenv(".env.local")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
if not ACCESS_TOKEN:
    raise RuntimeError("ACCESS_TOKEN no está configurado en las variables de entorno.")
sdk = mercadopago.SDK(ACCESS_TOKEN)


async def cancel_payment_preference(preference_id: str):
    """
    Cancela una preferencia de pago en Mercado Pago utilizando el ID de la preferencia.
    """
    try:
        preference_url = f"https://api.mercadopago.com/v1/payments/{preference_id}"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                preference_url, headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
            )
            if response.status_code == 200:
                payment_info = response.json()
                if payment_info.get("status") not in [
                    "approved",
                    "pending",
                ]:  # Condición de cancelación
                    cancel_url = f"https://api.mercadopago.com/v1/payments/{preference_id}/cancel"
                    cancel_response = await client.post(
                        cancel_url, headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
                    )

                    if cancel_response.status_code == 200:
                        return cancel_response.json()
                    else:
                        raise Exception(
                            f"Error cancelando la preferencia: {cancel_response.text}"
                        )
            else:
                raise Exception(
                    f"Error obteniendo información de la preferencia: {response.text}"
                )

    except Exception as e:
        raise Exception(f"Error al cancelar la preferencia: {e}")


async def get_payment_info(payment_id: str) -> dict:
    """
    Obtiene información de pago de Mercado Pago.

    Args:
        payment_id (str): ID del pago.

    Returns:
        dict: Detalles del pago.

    Raises:
        HTTPException: Si ocurre un error al obtener la información del pago.
    """
    url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()

        raise HTTPException(
            status_code=response.status_code,
            detail=f"Error al obtener información del pago: {response.text}",
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error de conexión al obtener información del pago: {e}",
        )


def validate_reservations(db: Session, reservations_list: List[str]) -> None:
    """
    Valida si los horarios solicitados ya están reservados en la base de datos.

    Args:
        db (Session): Sesión de la base de datos.
        reservations_list (List[str]): Lista de horarios solicitados.

    Raises:
        HTTPException: Si hay conflictos con los horarios ya reservados.
    """
    conflicts = (
        db.query(Reservation.reserved_times)
        .filter(Reservation.reserved_times.in_(reservations_list))
        .all()
    )

    # Extraer los horarios conflictivos
    already_reserved_times = [conflict.reserved_times for conflict in conflicts]

    if already_reserved_times:
        raise HTTPException(
            status_code=400,
            detail=(
                "Algunos horarios ya están reservados: "
                f"{', '.join(sorted(already_reserved_times))}. "
                "Por favor, seleccione horarios diferentes."
            ),
        )


def convert_to_iso8601(reservation_times: List) -> List[str]:
    """
    Convierte una lista de horarios a formato ISO8601.

    Args:
        reservation_times (List): Lista de horarios en formato datetime o string.

    Returns:
        List[str]: Horarios convertidos a ISO8601.

    Raises:
        ValueError: Si algún elemento no es un formato de fecha válido.
    """
    iso_times = []
    for res in reservation_times:
        try:
            if isinstance(res, str):
                # Intentar convertir desde string
                iso_times.append(datetime.fromisoformat(res).isoformat())
            elif isinstance(res, datetime):
                # Usar isoformat directamente si ya es datetime
                iso_times.append(res.isoformat())
            else:
                raise ValueError(f"Formato no válido para la fecha: {res}")
        except ValueError as e:
            raise ValueError(
                f"Error al convertir '{res}' a formato ISO8601: {e}"
            ) from e

    return iso_times


{
    "reservations": [
        {"reservation_hours": "2024-01-07T10:00:00"},
        {"reservation_hours": "2024-01-07T11:00:00"},
    ],
    "payment_type": "minimo",
}
