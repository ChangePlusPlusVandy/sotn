from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(engine)


def get_db():
    with SessionLocal() as db:
        yield db


DbSession = Annotated[Session, Depends(get_db)]
