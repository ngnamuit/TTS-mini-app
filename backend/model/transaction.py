
from sqlalchemy import Column, Integer, String, VARCHAR, Float, DateTime
from sqlalchemy.orm import Session
from .database import BaseWithDB

class TransactionModel(BaseWithDB):
    """
    'Use String instead of VARCHAR':
        String is part of SQLAlchemy's ORM design, which is meant to abstract the underlying SQL.
        It provides a cleaner, more Pythonic way to define column types without coupling your code too closely to the database-specific syntax.
    """
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(50), index=True)  # Limit length to 50
    customer_id = Column(String(50), index=True)  # Limit length to 50
    product_id = Column(String(50), index=True)  # Limit length to 50
    category = Column(String(100), index=True)  # Limit length to 100
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    country = Column(String(50), nullable=False)  # Limit length to 50
    total_price = Column(Float, nullable=False)

    @classmethod
    def create(cls, data: dict):
        """Insert a new transaction into the database."""
        db = next(cls.get_db())  # Retrieve the session from the generator
        try:
            new_transaction = cls(**data)
            db.add(new_transaction)
            db.commit()
            db.refresh(new_transaction)
            return new_transaction
        except Exception as error:
            db.rollback()
            print(f"[CREATE][ERROR]: {str(error)}")
            return None
        finally:
            db.close()  # Ensure the session is closed

    @classmethod
    def create_multi(cls, data: list):
        """
        Efficiently insert multiple rows using SQLAlchemy's bulk_insert_mappings.
        """
        db = next(cls.get_db())  # Retrieve the session from the generator
        try:
            db.bulk_insert_mappings(cls, data)
            db.commit()
            return True
        except Exception as error:
            db.rollback()
            print(f"[BULK INSERT][ERROR]: {str(error)}")
            return None
        finally:
            db.close()  # Ensure the session is closed

    @classmethod
    def get_all(cls, skip: int = 0, limit: int = 10):
        """Retrieve a list of transactions."""
        db = next(cls.get_db())  # Retrieve the session from the generator
        try:
            return db.query(cls).offset(skip).limit(limit).all()
        except Exception as error:
            print(f"[GET ALL][ERROR]: {str(error)}")
            return None
        finally:
            db.close()  # Ensure the session is closed

    @classmethod
    def get_by_id(cls, transaction_id: int):
        """Retrieve a transaction by its ID."""
        db = next(cls.get_db())  # Retrieve the session from the generator
        try:
            return db.query(cls).filter(cls.id == transaction_id).first()
        except Exception as error:
            print(f"[GET BY ID][ERROR]: {str(error)}")
            return None
        finally:
            db.close()  # Ensure the session is closed

    @classmethod
    def update(cls, transaction_id: int, updates: dict):
        """Update a transaction's details."""
        db = next(cls.get_db())  # Retrieve the session from the generator
        try:
            transaction = db.query(cls).filter(cls.id == transaction_id).first()
            if not transaction:
                return None
            for key, value in updates.items():
                setattr(transaction, key, value)
            db.commit()
            db.refresh(transaction)
            return transaction
        except Exception as error:
            db.rollback()
            print(f"[UPDATE][ERROR]: {str(error)}")
            return None
        finally:
            db.close()  # Ensure the session is closed

    @classmethod
    def delete(cls, transaction_id: int):
        """Delete a transaction by its ID."""
        db = next(cls.get_db())  # Retrieve the session from the generator
        try:
            transaction = db.query(cls).filter(cls.id == transaction_id).first()
            if not transaction:
                return None
            db.delete(transaction)
            db.commit()
            return transaction
        except Exception as error:
            db.rollback()
            print(f"[DELETE][ERROR]: {str(error)}")
            return None
        finally:
            db.close()  # Ensure the session is closed
