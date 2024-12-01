# db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL = (
    "mysql+mysqlconnector://root:devfranco2018@localhost:3306/futbol5db"
)


engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


# Función que proporciona una sesión de base de datos para las operaciones.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
