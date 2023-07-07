"""SQLAlchemy one-to-many relationship with multiple foreign keys.

https://avacariu.me/writing/2019/composite-foreign-keys-and-many-to-many-relationships-in-sqlalchemy
"""

from pathlib import Path
from typing import List

from sqlalchemy import (
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
    Table,
    create_engine,
    select,
)
from sqlalchemy.orm import Session, declarative_base, relationship

Base = declarative_base()


class Author(Base):
    """An author is identified by their userid and username."""

    __tablename__ = "author"

    userid = Column(Integer, primary_key=True)
    username = Column(String(30), primary_key=True)

    recipes = relationship(
        "Recipe",
        back_populates="author",
        # foreign_keys=[userid, username],
        # primaryjoin="and_(Recipe.author_userid==Author.userid, Recipe.author_username==Author.username)",
    )


class Recipe(Base):
    """A recipe is identified by its id and title."""

    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True)
    title = Column(String(30))

    # author_userid = Column(Integer, ForeignKey("author.userid"), nullable=False)
    # author_username = Column(String(30), ForeignKey("author.username"), nullable=False)

    author_userid = Column(Integer, nullable=False)
    author_username = Column(String(30), nullable=False)

    author = relationship(
        "Author",
        back_populates="recipes",
        # primaryjoin="and_(Recipe.author_userid==Author.userid, Recipe.author_username==Author.username)",
        # foreign_keys=[author_userid, author_username],
    )

    # this produces
    # FOREIGN KEY(author_userid, author_username) REFERENCES author (userid, username)
    # which I kinda like more than the double references
    # FOREIGN KEY(author_userid) REFERENCES author (userid),
    # FOREIGN KEY(author_username) REFERENCES author (username)
    __table_args__ = (
        ForeignKeyConstraint(
            ["author_userid", "author_username"],
            ["author.userid", "author.username"],
        ),
    )


# Create the database and engine
sqlite_file_name = "local_o2m_sa_dup.db"
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
        author = Author(userid=1, username="spongebob")
        recipe = Recipe(id=1, title="Krabby Patty", author=author)
        session.add(recipe)
        session.commit()
        print(f"\nDONE\n")
        print(f"\nADDED RECIPE: {recipe.title}")


def main() -> None:
    """Main function."""
    create_db_and_tables()
    create_and_select()


if __name__ == "__main__":
    main()
