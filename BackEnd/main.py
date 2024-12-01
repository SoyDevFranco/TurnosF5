# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import Base, engine
from routers.users_router import router as users_router
from routers.payments_router import router as payments_router
from routers.google_auth_router import router as google_auth_router

# Importar todos los modelos explícitamente
import models.users
import models.payment
import models.reservations


# Inicializar la aplicación FastAPI
app = FastAPI()

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Agregar el middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://6001-2803-9800-9024-7c0f-9484-1c8-5bc3-f86c.ngrok-free.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir los routers
app.include_router(payments_router)
app.include_router(google_auth_router, prefix="/auth")
app.include_router(users_router)


@app.get("/")
def root():
    return {"message": "Bienvenido a la Aplicación"}
