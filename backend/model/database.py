from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL
DATABASE_URL = "postgresql://odoo:odoo@localhost:5434/tts_app"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
class BaseWithDB(Base):
    __abstract__ = True  # Ensure this base isn't treated as a table

    @classmethod
    def get_db(cls):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
