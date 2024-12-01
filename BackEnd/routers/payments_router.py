# routers/payments_router.py
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user
from db.database import get_db
from schemas.reservations import ReservationRequest
from controllers.payment import create_total_amount, create_mercadopago_preference
from controllers.utils import (
    convert_to_iso8601,
    get_payment_info,
    validate_reservations,
    cancel_payment_preference,
)
from controllers.redis_service import (
    save_to_redis,
    read_from_redis,
    save_intención_pago,
    read_intención_pago,
)
from controllers.saveData import Save
import httpx  # Para hacer las peticiones HTTP
import uuid

# Crear el router para los endpoints
router = APIRouter()


# http://127.0.0.1:8003/create_order
# {
#   "reservations": [
#     {
#       "reservation_hours": "2024-01-07T10:00:00"
#     },
#     {
#       "reservation_hours": "2024-01-07T11:00:00"
#     }
#   ],
#   "payment_type": "minimo"
# }
@router.post("/create_order")
def create_order_endpoint(
    reservation_request: ReservationRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Crea una orden de pago en Mercado Pago para las reservas solicitadas,
    almacena la solicitud en Redis y genera una URL con identificador único.
    """
    try:
        user_id = current_user.id
        print(f"User id: {type(user_id)} {user_id}")
        # reservations_list = ["ejemplo_1","ejemplo_2"]
        reservations_list = convert_to_iso8601(
            [
                reservation.reservation_hours
                for reservation in reservation_request.reservations
            ]
        )

        # Validar horarios reservados
        validate_reservations(db, reservations_list)

        # Guardar la solicitud completa en Redis con el identificador

        print(f"Guardando datos en Redis bajo la clave: {user_id}")
        # KEY = user_id(1), ["ejemplo_1","ejemplo_2"]

        # Calcular el monto total a pagar
        amount_to_pay = create_total_amount(reservation_request)

        # Crear la preferencia de pago incluyendo el identificador único en la URL de notificación
        payment_order = create_mercadopago_preference(amount_to_pay, user_id)
        payment_url = payment_order.get("init_point")
        preference_id = payment_order.get("id")
        print(f"Preference id: {preference_id}")
        # Generar un key único usando UUID
        key_uuid = str(uuid.uuid4())
        save_intención_pago(key=key_uuid, data=preference_id)
        save_to_redis(key=user_id, data=reservations_list)

        return {"payment_url": payment_url}

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear la orden de pago")


# Ruta Webhook
@router.post("/webhook")
async def webhook_handler(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Maneja las notificaciones de Mercado Pago y cancela la intención de pago si expiró.
    """
    try:
        user_id = request.query_params.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=400, detail="El parámetro 'user_id' es obligatorio."
            )

        # Recuperar los datos de Redis usando la clave user_id
        reservations_list = read_from_redis(key=user_id)  # ["ejemplo_1","ejemplo_2"]
        preference_id = read_intención_pago(key=user_id)
        if preference_id:
            await cancel_payment_preference(preference_id)

        # Leer los datos del request si la intención de pago es válida
        data = await request.json()
        payment_id = data.get("data", {}).get("id")
        payment_info = await get_payment_info(payment_id)
        amount_paid = payment_info.get("transaction_amount")

        # Guardar los datos en la base de datos
        save_instance = Save(db, user_id, payment_id, amount_paid, reservations_list)
        save_instance.all_save()

        return {"message": "Notificación procesada exitosamente"}

    except HTTPException as e:
        raise e

    except Exception as e:
        print(f"Error procesando el webhook: {e}")
        raise HTTPException(status_code=500, detail=f"Error procesando webhook: {e}")
