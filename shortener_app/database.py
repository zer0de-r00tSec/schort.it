from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import get_settings

DB_USERNAME = get_settings().DB_USERNAME
DB_PASSWORD = get_settings().DB_PASSWORD
DB_HOST = get_settings().DB_HOST
DB_DATABASE = get_settings().DB_DATABASE

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"

# Engine erstellen
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Verbindung testen
try:
    # Versuche eine Verbindung zu erstellen
    with engine.connect() as connection:
        print("Datenbankverbindung erfolgreich!")
except exc.SQLAlchemyError as e:
    print(f"Fehler bei der Verbindung zur Datenbank: {e}")

# Dependency für die Datenbank-Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()