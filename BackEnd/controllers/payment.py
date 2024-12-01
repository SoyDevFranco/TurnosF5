# controllers/payment.py
import mercadopago
import os
from dotenv import load_dotenv
from schemas.reservations import ReservationRequest

# Cargar variables de entorno
load_dotenv(".env.local")
access_token = os.getenv("ACCESS_TOKEN")

if not access_token:
    raise ValueError("ACCESS_TOKEN no está configurado en las variables de entorno.")

sdk = mercadopago.SDK(access_token)

# Constantes de precios para el cálculo de montoss
PRICE_MIN_PER_RESERVATION = 5000
PRICE_TOTAL_PER_RESERVATION = 20000

# URLs configurables
BASE_URL = os.getenv("BASE_URL", "http://localhost:5173/")
NOTIFICATION_BASE_URL = (
    "https://4bef-2803-9800-9024-7c0f-9484-1c8-5bc3-f86c.ngrok-free.app"
)


def calculate_payment_limits(total_reservations: int) -> tuple[int, int]:
    """
    Calcula los límites de pago según el número de reservas.
    """
    if total_reservations <= 0:
        raise ValueError("El número de reservas debe ser mayor a cero.")

    min_amount = total_reservations * PRICE_MIN_PER_RESERVATION
    max_amount = total_reservations * PRICE_TOTAL_PER_RESERVATION
    return min_amount, max_amount


from datetime import datetime, timedelta
import pytz


def create_mercadopago_preference(amount: int, user_id: int) -> dict:
    """
    Crea una preferencia de pago en Mercado Pago, incluyendo un identificador único
    y un período de vigencia para la preferencia.
    """
    if amount <= 0:
        raise ValueError("El monto debe ser mayor a cero.")
    print("key_redis", user_id)

    # Incluir el identificador único en la URL de notificación
    notification_url = f"{NOTIFICATION_BASE_URL}/webhook?user_id={user_id}"

    print("notification_url", notification_url)

    # Obtener la fecha y hora actuales en formato ISO 8601
    now = datetime.now(pytz.timezone("America/Argentina/Buenos_Aires"))
    expiration_from = now.isoformat()

    # Definir la fecha de vencimiento, por ejemplo, 30 días después de la fecha de inicio
    expiration_to = (now + timedelta(seconds=30)).isoformat()

    preference_data = {
        "items": [
            {
                "title": "Reserva de cancha",
                "currency_id": "ARS",
                "unit_price": amount,
                "quantity": 1,
            }
        ],
        "back_urls": {
            "success": f"{BASE_URL}/success",
            "failure": f"{BASE_URL}/failure",
            "pending": f"{BASE_URL}/pending",
        },
        "notification_url": notification_url,
        "auto_return": "approved",
        "expires": True,  # Activar la expiración
        "expiration_date_from": expiration_from,  # Fecha y hora de inicio
        "expiration_date_to": expiration_to,  # Fecha y hora de vencimiento
    }

    preference_response = sdk.preference().create(preference_data)

    if (
        "response" not in preference_response
        or "id" not in preference_response["response"]
    ):
        raise ValueError(
            f"Error al crear la preferencia en Mercado Pago: {preference_response}"
        )

    print("preference_response", preference_response)

    return preference_response["response"]


def create_total_amount(reservation_request: ReservationRequest) -> dict:
    """
    Crea la orden de pago en Mercado Pago para la reserva.
    """
    if not isinstance(reservation_request, (ReservationRequest, dict)):
        raise TypeError(
            "reservation_request debe ser un diccionario o un objeto de tipo ReservationRequest."
        )

    # Obtener tipo de pago
    payment_type = reservation_request.payment_type

    # Calcular total de reservas
    total_reservations = (
        len(reservation_request["reservations"])
        if isinstance(reservation_request, dict)
        else len(reservation_request.reservations)
    )
    if total_reservations <= 0:
        raise ValueError("Debe haber al menos una reserva.")

    # Calcular montos
    min_amount, max_amount = calculate_payment_limits(total_reservations)
    amount_to_pay = min_amount if payment_type == "minimo" else max_amount

    return amount_to_pay
