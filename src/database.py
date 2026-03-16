import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "sqlite:///./docs.db"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./docs.db")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)  # verify connection
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
