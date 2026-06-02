"""
Database configuration

Contains:
- SQLAlchemy engine
- Session factory
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite://task_tracker.db"


# Engine manages connections to the database
engine = create_engine(
    DATABASE_URL,
    echo=False,
)

# Factory that creates DB sessions
SessionLocal = sessionmaker(
    bing=engine,
    autoflush=False,
    autocommit=False,
)