from sqlalchemy import Boolean, Column, Integer, String, Text
from .database import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    target_url = Column(Text, index=True)  # Text statt String, falls URL länger ist
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0, index=True)  # Index für 'clicks' hinzugefügt
    date = Column(Integer)