# auth/auth_base.py
from fastapi import APIRouter, HTTPException, Depends, status
from jose import jwt, JWTError
from datetime import datetime, timedelta
import requests


# Inicializar el enrutador para las rutas de autenticación
router = APIRouter()

# Constantes de configuración de Google y JWT
GOOGLE_CLIENT_ID = (
    "277449645968-7q19lqbsb10cvoasbgp4pevqvnnnjttn.apps.googleusercontent.com"
)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
JWT_SECRET_KEY = "my_jwt_secret_key"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60
_cached_openid_config = None


def get_google_openid_config():
    """
    Obtiene y almacena en caché la configuración OpenID de Google.
    """
    global _cached_openid_config
    if _cached_openid_config is None:
        _cached_openid_config = requests.get(GOOGLE_DISCOVERY_URL).json()
    return _cached_openid_config


def verify_google_token(token: str):
    """
    Verifica y decodifica el token de Google para autenticación.
    - Obtiene la URI de las claves públicas de Google desde la configuración OpenID.
    - Decodifica el token usando las claves públicas y valida el cliente (audience).
    """
    openid_config = get_google_openid_config()
    jwks_uri = openid_config.get("jwks_uri")

    try:
        response = requests.get(jwks_uri)
        keys = response.json().get("keys")
        payload = jwt.decode(
            token, keys, algorithms=["RS256"], audience=GOOGLE_CLIENT_ID
        )
        return payload
    except JWTError as jwt_error:
        # Error de formato de token JWT
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format"
        ) from jwt_error
    except requests.RequestException as req_error:
        # Error en la solicitud a la URI de claves públicas
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate Google token",
        ) from req_error


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Genera un token de acceso JWT.
    - data: Información a incluir en el token.
    - expires_delta: Tiempo de expiración del token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=JWT_EXPIRATION_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt
