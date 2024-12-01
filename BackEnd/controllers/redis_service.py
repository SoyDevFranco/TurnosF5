# controllers/redis_service.py
from config.redis_connection import redis_manager
import json

# Obtener instancia de Redis
redis_client = redis_manager()


# Guardar un JSON (dict/list) en Redis
def save_to_redis(key: int, data: dict | list, expiration: int = 50):
    """
    Guarda un JSON (dict o list) en Redis con una clave y tiempo de expiración.
    """
    if redis_client:
        try:
            print(f"Guardando datos en Redis bajo la clave '{key}'")
            redis_client.set(key, json.dumps(data), ex=expiration)
            print(f"Datos json.dumps: {json.dumps(data)}")
        except Exception as e:
            print(f"Error al guardar en Redis: {e}")


# Leer un valor de Redis
def read_from_redis(key: int):
    """
    Lee un valor de Redis dado un key.
    """
    if redis_client:
        try:
            data = redis_client.get(key)
            if data:
                print(f"Datos recuperados del read: {data}")
                return json.loads(data)
            else:
                print(f"No se encontró ningún dato bajo la clave '{key}'")
        except Exception as e:
            print(f"Error al leer desde Redis: {e}")


# Eliminar un valor de Redis
def delete_from_redis(key: int):
    """
    Elimina un valor en Redis por clave.
    """
    if redis_client:
        try:
            redis_client.delete(key)
            print(f"Clave '{key}' eliminada de Redis")
        except Exception as e:
            print(f"Error al eliminar en Redis: {e}")


def save_intención_pago(key: int, data: dict, expire_time: int = 3000):
    """
    Guarda el preference_id con datos asociados en Redis con un tiempo de expiración.

    :param preference_id: El ID único de la preferencia.
    :param data: Los datos asociados que se guardarán (dict).
    :param expire_time: Tiempo en segundos antes de que la clave expire (por defecto 600s = 10 minutos).
    """
    try:

        redis_client.set(key, json.dumps(data), ex=expire_time)
        print(f"Guardado en Redis: {data} con expiración de {expire_time} segundos.")
    except Exception as e:
        print(f"Error al guardar el preference_id en Redis: {e}")
        raise


def read_intención_pago(key: int):
    """
    Lee los datos asociados a un preference_id desde Redis.

    :param preference_id: El ID único de la preferencia.
    :return: Los datos asociados al preference_id o None si no existe.
    """
    if redis_client:
        try:
            data = redis_client.get(key)
            if data:
                print(f"Datos recuperados del readIntencionPago: {data}")
                return json.loads(data)
        except Exception as e:
            print(f"Error al leer el intencion de pago: {e}")
            raise
