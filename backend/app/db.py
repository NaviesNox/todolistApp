from __future__ import annotations

import os

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

load_dotenv()


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", "sqlite:///./todo.db")


def create_db_engine():
    url = get_database_url()
    connect_args = {}
    if url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
    return create_engine(url, echo=False, connect_args=connect_args)


engine = create_db_engine()


def get_session():
    with Session(engine) as session:
        yield session

