from sqlalchemy.orm import Session
from . import keygen, models, schemas
import time

def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    key = keygen.create_unique_random_key(db)
    secret_key = f"{key}_{keygen.create_random_key(length=8)}"
    db_url = models.URL(
        date=time.time(),
        target_url=url.target_url,
        key=key,
        secret_key=secret_key,
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_db_url_by_key(db: Session, url_key: str) -> models.URL | None:
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active == True)
        .first()
    )

def update_db_clicks(db: Session, db_url: models.URL) -> models.URL:
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url

def get_db_url_by_secret_key(db: Session, secret_key: str, include_inactive: bool = False):
    query = db.query(models.URL).filter(models.URL.secret_key == secret_key)
    if not include_inactive:
        query = query.filter(models.URL.isactive == True)
    return query.first()

# Admin Button toggle
def deactivate_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL | None:
    db_url = get_db_url_by_secret_key(db, secret_key, include_inactive=True)
    if not db_url:
        return None
    db_url.is_active = False
    db.commit()
    db.refresh(db_url)
    return db_url

def reactivate_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL | None:
    db_url = get_db_url_by_secret_key(db, secret_key, include_inactive=True)
    if not db_url:
        return None
    db_url.is_active = True
    db.commit()
    db.refresh(db_url)
    return db_url

# Admin delete Button
def delete_db_url_by_secret_key(db: Session, secret_key: str) -> bool:
    db_url = get_db_url_by_secret_key(db, secret_key)
    if not db_url:
        return False
    db.delete(db_url)
    db.commit()
    return True

