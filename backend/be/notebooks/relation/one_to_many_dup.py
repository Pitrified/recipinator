"""Test one to many relationship using two foreign keys."""

from pathlib import Path
from sqlmodel import (
    Field,
    ForeignKey,
    ForeignKeyConstraint,
    Relationship,
    Session,
    SQLModel,
    create_engine,
)

auth_rec_join = (
    "and_("
    "Recipe.author_userid==Author.userid"
    ", Recipe.author_username==Author.username)"
)


class Author(SQLModel, table=True):
    """An author is identified by a userid and a username."""

    userid: int = Field(primary_key=True)
    username: str = Field(primary_key=True)

    # recipes: list["Recipe"] = Relationship(back_populates="author")
    recipes: list["Recipe"] = Relationship(
        back_populates="author",
        # sa_relationship_kwargs={"foreign_keys": [userid, username]}
        # sa_relationship_kwargs={"foreign_keys": ["userid", "username"]},
        # "primaryjoin": "Recipe.author_userid==Author.userid AND Recipe.author_username==Author.username"
        sa_relationship_kwargs={"primaryjoin": auth_rec_join},
    )


class Recipe(SQLModel, table=True):
    """A recipe is identified by a recipeid."""

    recipeid: int = Field(primary_key=True)
    title: str

    author_userid: int | None = Field(foreign_key="author.userid", default=None)
    author_username: str | None = Field(foreign_key="author.username", default=None)

    # author_userid: int | None = Field(default=None)
    # author_username: str | None = Field(default=None)

    # author: Author | None = Relationship(back_populates="recipes")
    author: Author | None = Relationship(
        back_populates="recipes",
        # sa_relationship_kwargs={"foreign_keys": [author_userid, author_username]},
        # sa_relationship_kwargs={
        # sa_relationship_kwargs={ "primaryjoin": "Recipe.author_userid==Author.userid AND Recipe.author_username==Author.username" },
        sa_relationship_kwargs={"primaryjoin": auth_rec_join},
    )

    # author_userid: int = Field(foreign_key=ForeignKey("author.userid"), default=None)
    # author_username: str = Field(foreign_key=ForeignKey("author.username"), default=None)

    __table_args__ = (
        ForeignKeyConstraint(
            ["author_userid", "author_username"],
            ["author.userid", "author.username"],
        ),
    )


# Create the database and engine
sqlite_file_name = "local_o2m_dup.db"
sqlite_fp = Path(sqlite_file_name)
if sqlite_fp.exists():
    sqlite_fp.unlink()
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables() -> None:
    """Set up the database and tables."""
    SQLModel.metadata.create_all(engine)


# def create_author() -> None:
#     with Session(engine) as session:
#         # create author
#         author = Author(userid=1, username="author1")
#         session.add(author)
#         session.commit()


def create_author_recipe() -> None:
    """Create authors and recipes."""
    with Session(engine) as session:
        # create author
        author = Author(userid=1, username="author1")

        # create recipe
        # this does not raise an error, but leaves the userid and username as None
        recipe = Recipe(recipeid=1, title="recipe1", author=author)

        # add only the recipe to the session
        session.add(recipe)
        print(f"\nADDED RECIPE: {recipe}")

        # commit all
        session.commit()

        # refresh the recipe to see the author
        session.refresh(recipe)
        print(recipe)

        # # commit all
        # session.commit()


def main() -> None:
    """Run the main program."""
    create_db_and_tables()
    # create_author()
    create_author_recipe()


if __name__ == "__main__":
    main()

# raises
# sqlalchemy.exc.AmbiguousForeignKeysError: Could not determine join condition between parent/child tables on relationship Author.recipes - there are multiple foreign key paths linking the tables.  Specify the 'foreign_keys' argument, providing a list of those columns which should be counted as containing a foreign key reference to the parent table.
