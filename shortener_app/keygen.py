import secrets
import string
from sqlalchemy.orm import Session
from . import crud

# Erzeugt einen zufälligen Schlüssel mit Großbuchstaben und Zahlen
def create_random_key(length: int = 8) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))

# Erzeugt einen einzigartigen zufälligen Schlüssel, der noch nicht in der DB existiert
def create_unique_random_key(db: Session) -> str:
    # Generiere einen zufälligen Schlüssel
    key = create_random_key()
    
    # Überprüfe, ob der Schlüssel bereits existiert, und generiere bei Bedarf einen neuen
    while crud.get_db_url_by_key(db, key):
        key = create_random_key()
    
    # Gib den einzigartigen Schlüssel zurück
    return key
