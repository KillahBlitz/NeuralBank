import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = (
    f"postgresql+psycopg2://"
    f"{os.environ['DB_POSTGRES_USER']}:{os.environ['DB_POSTGRES_PASSWORD']}"
    f"@{os.environ['DB_POSTGRES_HOST']}:{os.environ['DB_POSTGRES_PORT']}"
    f"/{os.environ['DB_POSTGRES_DB']}"
)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()