import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings

# For this MVP, we will use a local SQLite database by default to ensure the demo works seamlessly
# without needing Postgres running, but we allow overriding via DATABASE_URL.
# If DATABASE_URL is postgres, we'll use that.
db_url = os.getenv("DATABASE_URL", "sqlite:///./mentora.db")

connect_args = {}
if db_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(db_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
