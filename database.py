from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
    "sqlite:///db.sqlite3", connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_database() -> SessionLocal:
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


def proceed_changes(db: Session = None, obj: object = None) -> None:
    db.add(obj)
    db.commit()
    db.refresh(obj)
