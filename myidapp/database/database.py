from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . import models

# database_settings = get_database_settings()

# SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{database_settings.DB_USERNAME}:{database_settings.DB_PASSWORD}@{database_settings.DB_HOST}/{database_settings.DB_NAME}"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/stock"
SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
