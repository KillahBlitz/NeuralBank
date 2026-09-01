import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

DB_URL = (
    f"postgresql+psycopg2://"
    f"{os.environ['DB_POSTGRES_USER']}:{os.environ['DB_POSTGRES_PASSWORD']}"
    f"@{os.environ['DB_POSTGRES_HOST']}:{os.environ['DB_POSTGRES_PORT']}"
    f"/{os.environ['DB_POSTGRES_DB']}"
)

engine = create_engine(DB_URL, pool_pre_ping=True)
_session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = scoped_session(_session_factory)
Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)


def remove_session():
    SessionLocal.remove()