"""SQLModel one to many relationship using one foreign key and unique constraint."""

from pathlib import Path

from sqlmodel import (
    Field,
    Relationship,
    Session,
    SQLModel,
    UniqueConstraint,
    create_engine,
    select,
)


class Author(SQLModel, table=True):
    """An author is identified by a userid and a username."""

    id: int | None = Field(primary_key=True, default=None)

    userid: int
    username: str

    age: int | None = Field(default=None, nullable=True)

    recipes: list["Recipe"] = Relationship(back_populates="author")

    # constrain the userid and username to be unique
    __table_args__ = (UniqueConstraint("userid", "username"),)


class Recipe(SQLModel, table=True):
    """A recipe is identified by a recipeid."""

    id: int | None = Field(primary_key=True, default=None)

    recipeid: int
    title: str

    authorid: int | None = Field(foreign_key="author.id", default=None)
    author: Author = Relationship(back_populates="recipes")


sqlite_file_name = "local_o2m_unique.db"
sqlite_fp = Path(sqlite_file_name)
if sqlite_fp.exists():
    sqlite_fp.unlink()
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables() -> None:
    """Create the database and tables."""
    SQLModel.metadata.create_all(engine)


def create_author_recipe() -> None:
    """Create authors and recipes."""
    with Session(engine) as session:
        # create author
        author = Author(userid=1, username="author1")

        # create recipe
        recipe = Recipe(recipeid=1, title="recipe1", author=author)

        # add only the recipe to the session
        session.add(recipe)
        print(f"\nADDED RECIPE: {recipe}")

        # commit all
        session.commit()

        # refresh the recipe to see the author
        session.refresh(recipe)
        print(f"\nFRESH RECIPE: {recipe}")

        # select the author using userid and username
        author_load = session.exec(
            select(Author).where(Author.userid == 1).where(Author.username == "author1")
        ).first()
        print(f"\nSELECTED AUTHOR: {author_load}")

        # create another recipe with existing author
        # same author, with author.id from load
        if author_load:
            recipe2 = Recipe(recipeid=2, title="recipe2", author=author_load)
            session.add(recipe2)
            session.commit()


def main() -> None:
    """Create the database and tables, then create authors and recipes."""
    create_db_and_tables()
    create_author_recipe()


if __name__ == "__main__":
    main()
