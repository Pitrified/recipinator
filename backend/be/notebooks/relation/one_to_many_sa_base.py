"""SQLAlchemy one-to-many relationship example.

Note that we are on 1.4.41
https://docs.sqlalchemy.org/en/14/orm/quickstart.html
"""
from __future__ import annotations

from pathlib import Path
from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, Table, create_engine, select
from sqlalchemy.orm import Session, declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)
    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
    user = relationship("User", back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


# Create the database and engine
sqlite_file_name = "local_o2m_sa_base.db"
sqlite_fp = Path(sqlite_file_name)
if sqlite_fp.exists():
    sqlite_fp.unlink()
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables() -> None:
    """Set up the database and tables."""
    Base.metadata.create_all(engine)


def create_and_select() -> None:
    with Session(engine) as session:
        # create
        spongebob = User(
            name="spongebob",
            fullname="Spongebob Squarepants",
            addresses=[Address(email_address="spongebob@sqlalchemy.org")],
        )
        sandy = User(
            name="sandy",
            fullname="Sandy Cheeks",
            addresses=[
                Address(email_address="sandy@sqlalchemy.org"),
                Address(email_address="sandy@squirrelpower.org"),
            ],
        )
        patrick = User(name="patrick", fullname="Patrick Star")
        session.add_all([spongebob, sandy, patrick])
        session.commit()

        # simple select
        stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))
        print(f"\nSELECT sample ----------------------")
        for user in session.scalars(stmt):
            print(user)

        # select with join
        print(f"\nSELECT join   ----------------------")
        stmt = (
            select(Address)
            .join(Address.user)
            .where(User.name == "sandy")
            .where(Address.email_address == "sandy@sqlalchemy.org")
        )
        sandy_address = session.scalars(stmt).one()
        print(sandy_address)


def main() -> None:
    """Main function."""
    create_db_and_tables()
    create_and_select()


if __name__ == "__main__":
    main()
