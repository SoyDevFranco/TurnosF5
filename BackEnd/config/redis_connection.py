# config/redis_connection.py
from redis import Redis
from redis.exceptions import ConnectionError
from os import getenv


# Conectar a Redis con configuración desde variables de entorno
def redis_manager():
    try:
        redis_host = getenv("REDIS_HOST", "honest-hippo-33480.upstash.io")
        redis_port = int(getenv("REDIS_PORT", 6379))
        redis_password = getenv(
            "REDIS_PASSWORD",
            "AYLIAAIjcDEyODhjYThkYjJmNGQ0ODhlOTRkODJjODUzNDdlYjJjY3AxMA",
        )
        redis_ssl = True

        redis_client = Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            ssl=redis_ssl,
            decode_responses=True,  # Para recibir strings directamente
        )

        # Verificamos la conexión con un ping
        if redis_client.ping():
            print("Redis conectado exitosamente")
            return redis_client
        else:
            print("Falló el ping a Redis")
            return None

    except ConnectionError as e:
        print("Error de conexión a Redis:", e)
        return None

    except Exception as e:
        print("Error inesperado al conectar a Redis:", e)
        return None
