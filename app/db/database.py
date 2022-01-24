from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


uri = settings.SQLALCHEMY_DATABASE_URL
SQLALCHEMY_DATABASE_URL = uri.replace('postgres://', 'postgresql://', 1) if uri.startswith('postgres://') else uri

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
