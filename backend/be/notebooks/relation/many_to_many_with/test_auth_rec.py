"""Test the Author and Recipe models."""

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

from loguru import logger as lg

# # add local folder to path
# import sys
# sys.path.append(".")
# lg.debug(f"sys.path: {sys.path}")


# from be.notebooks.relation.many_to_many_with.Author import Author
# from be.notebooks.relation.many_to_many_with.Recipe import Recipe

####### AUTHOR #########################################


class AuthorBase(SQLModel):
    """Author Base."""

    userid: int
    username: str


class Author(AuthorBase, table=True):
    """Author in the db."""

    id: int | None = Field(default=None, primary_key=True)

    recipes: list["Recipe"] = Relationship(
        back_populates="author",
    )

    # constrain the userid and username to be unique
    __table_args__ = (UniqueConstraint("userid", "username"),)


class AuthorCreate(AuthorBase):
    """Author Create."""


class AuthorRead(AuthorBase):
    """Author Read."""

    id: int


class AuthorUpdate(AuthorBase):
    """Author Update."""

    id: int | None = None

    userid: int | None = None
    username: str | None = None


class AuthorReadWithRecipes(AuthorRead):
    """Author Read With Recipes."""

    recipes: list["RecipeRead"]


####### RECIPE #########################################


class RecipeBase(SQLModel):
    """Recipe Base."""

    title: str
    caption: str

    author_id: int | None = Field(foreign_key="author.id", default=None)


class Recipe(RecipeBase, table=True):
    """Recipe in the db."""

    id: int | None = Field(default=None, primary_key=True)

    author: "Author" = Relationship(
        back_populates="recipes",
    )


class RecipeCreate(RecipeBase):
    """Recipe Create."""


class RecipeRead(RecipeBase):
    """Recipe Read."""

    id: int


class RecipeUpdate(RecipeBase):
    """Recipe Update."""

    id: int | None = None

    title: str | None = None
    caption: str | None = None

    author_id: int | None = None


class RecipeReadWithAuthor(RecipeRead):
    """Recipe Read With Author."""

    author: "AuthorRead"


####### TAG #########################################

####### RECIPE TAG LINK #########################################

####### MAIN TEST #########################################

sqlite_file_name = "local_m2m_attr.db"
sqlite_fp = Path(sqlite_file_name)
if sqlite_fp.exists():
    sqlite_fp.unlink()
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables() -> None:
    """Create the database and tables."""
    SQLModel.metadata.create_all(engine)


def create_author_recipe() -> None:
    """Create authors and recipes and tags."""
    with Session(engine) as session:
        # create author
        author1 = Author(userid=1, username="author1")

        # create recipe
        recipe1 = Recipe(
            title="recipe1",
            caption="caption1",
            author=author1,
        )

        # commit the recipe
        session.add(recipe1)
        session.commit()

        # refresh to get the id
        session.refresh(recipe1)

        # query
        query = select(Recipe).where(Recipe.id == recipe1.id)
        recipe1_ = session.exec(query).first()
        lg.debug(f"SELECT recipe: {recipe1_}\n")


def main() -> None:
    """Create the database and tables, then create authors and recipes."""
    create_db_and_tables()
    create_author_recipe()


if __name__ == "__main__":
    main()
