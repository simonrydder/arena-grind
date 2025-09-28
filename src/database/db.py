from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from database.models.base import Base

# SQLite file DB by default; swap URL in settings/env as needed
DATABASE_URL = "sqlite:///./arena_grind.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {},
    future=True,
)

# Thread-local sessions (plays well with FastAPI’s lifespan deps)
SessionLocal = scoped_session(
    sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
)


def create_all() -> None:
    """Create DB schema (use migrations for prod later)."""
    # Imported here to register model metadata before create_all

    Base.metadata.create_all(bind=engine)


@contextmanager
def session_scope() -> Iterator[Session]:
    # Session closes on exit; transaction commits on success, rolls back on error
    with SessionLocal() as session, session.begin():
        yield session


# FastAPI-friendly dependency
def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
