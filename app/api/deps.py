from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db import base as _db_base  # noqa: F401
from app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
