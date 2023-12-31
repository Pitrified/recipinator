"""Setup the database."""

# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     connect_args={"check_same_thread": False},
# )
# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine,
# )
# Base = declarative_base()

from typing import Any, Generator
from be.data.utils import get_resource
from sqlmodel import SQLModel, Session, create_engine

# sqlite_file_name = "database.db"
sqlite_file_name = str(get_resource("database_fp"))
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)


def create_db_and_tables() -> None:
    """Create the database and tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, Any, None]:
    """Get a session."""
    with Session(engine) as session:
        yield session
