"""SQLModel many to many relationship using link model as the Link table.

Use direct relationships between the main tables,
just referencing the link model as the Link table.
"""

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


class RecipeTagLink(SQLModel, table=True):
    """Link recipes and tags."""

    recipe_id: int | None = Field(
        primary_key=True,
        foreign_key="recipe.id",
        default=None,
    )
    tag_id: int | None = Field(
        primary_key=True,
        foreign_key="tag.id",
        default=None,
    )

    # confidence: float
    # origin: str

    # recipe: Recipe = Relationship(back_populates="tag_links")
    # tag: Tag = Relationship(back_populates="recipe_links")


class Recipe(SQLModel, table=True):
    """A recipe is identified by a recipe_id."""

    id: int | None = Field(primary_key=True, default=None)

    recipe_id: int
    title: str

    author_id: int | None = Field(foreign_key="author.id", default=None)
    author: Author = Relationship(back_populates="recipes")

    tags: list["Tag"] = Relationship(
        back_populates="recipes",
        link_model=RecipeTagLink,
    )


class Tag(SQLModel, table=True):
    """A tag."""

    id: int | None = Field(primary_key=True, default=None)

    name: str = Field(index=True, unique=True)
    description: str = Field(default="")
    usefulness: float = Field(default=0.0)

    recipes: list[Recipe] = Relationship(
        back_populates="tags",
        link_model=RecipeTagLink,
    )


sqlite_file_name = "local_m2m_rel.db"
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
        author = Author(userid=1, username="author1")

        # create tags
        tag1 = Tag(name="tag1", usefulness=0.5)
        tag2 = Tag(name="tag2")

        # create recipe
        recipe = Recipe(
            recipe_id=1,
            title="recipe1",
            author=author,
            tags=[tag1, tag2],
        )

        # add only the recipe to the session
        session.add(recipe)
        print(f"ADDED RECIPE: {recipe}\n")

        # commit all
        session.commit()

        # refresh the recipe to see the author id
        session.refresh(recipe)
        print(f"FRESH RECIPE: {recipe}\n")
        # when we access the fields, the author and tags are loaded with a new query
        print(f"FRESH RECIPE AUTHOR: {recipe.author}\n")
        print(f"FRESH RECIPE TAGS: {recipe.tags}\n")

        # select the author using userid and username
        author_load = session.exec(
            select(Author).where(Author.userid == 1).where(Author.username == "author1")
        ).first()
        print(f"SELECTED AUTHOR: {author_load}\n")

        # select the tag using name
        tag_load = session.exec(select(Tag).where(Tag.name == "tag1")).first()
        print(f"SELECTED TAG: {tag_load}\n")

        # create another recipe with existing author
        # same author, with author.id from load
        if author_load:
            recipe2 = Recipe(recipe_id=2, title="recipe2", author=author_load)
            session.add(recipe2)
            session.commit()


def main() -> None:
    """Create the database and tables, then create authors and recipes."""
    create_db_and_tables()
    create_author_recipe()


if __name__ == "__main__":
    main()
