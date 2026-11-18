"""
EdgeVision - Veritabanı Bağlantısı ve Modelleri
"""
import os
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://edgevision:edgevision@postgres:5432/edgevision")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PredictionLog(Base):
    __tablename__ = "prediction_logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    model_name = Column(String)
    inference_ms = Column(Float)
    detection_count = Column(Integer)
    image_width = Column(Integer)
    image_height = Column(Integer)

# Tabloları oluştur
Base.metadata.create_all(bind=engine)
