"""SQLModel many to many relationship using links in the main tables."""

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

    # attributes of the link
    confidence: float
    origin: str

    recipe: "Recipe" = Relationship(back_populates="tag_links")
    tag: "Tag" = Relationship(back_populates="recipe_links")


class Recipe(SQLModel, table=True):
    """A recipe is identified by a recipe_id."""

    id: int | None = Field(primary_key=True, default=None)

    recipe_id: int
    title: str

    author_id: int | None = Field(foreign_key="author.id", default=None)
    author: Author = Relationship(back_populates="recipes")

    tag_links: list[RecipeTagLink] = Relationship(back_populates="recipe")


class Tag(SQLModel, table=True):
    """A tag."""

    id: int | None = Field(primary_key=True, default=None)

    name: str = Field(index=True, unique=True)
    description: str = Field(default="")
    usefulness: float = Field(default=0.0)

    recipe_links: list[RecipeTagLink] = Relationship(back_populates="tag")


sqlite_file_name = "local_m2m_attr.db"
sqlite_fp = Path(sqlite_file_name)
if sqlite_fp.exists():
    sqlite_fp.unlink()
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables() -> None:
    """Create the database and tables."""
    SQLModel.metadata.create_all(engine)


def create_author_recipe_tag() -> None:
    """Create authors and recipes and tags."""
    with Session(engine) as session:
        # create author
        author1 = Author(userid=1, username="author1")

        # create tags
        tag1 = Tag(name="tag1", usefulness=0.5)
        tag2 = Tag(name="tag2")

        # create recipe
        recipe1 = Recipe(
            recipe_id=1,
            title="recipe1",
            author=author1,
        )

        # create links
        recipe_tag_link1 = RecipeTagLink(
            recipe=recipe1,
            tag=tag1,
            confidence=0.9,
            origin="user",
        )
        recipe_tag_link2 = RecipeTagLink(
            recipe=recipe1,
            tag=tag2,
            confidence=0.5,
            origin="GPT",
        )

        # save to database
        session.add(recipe_tag_link1)
        session.add(recipe_tag_link2)
        session.commit()

        # query
        query = select(Recipe).where(Recipe.id == recipe1.id)
        recipe_ = session.exec(query).first()
        lg.debug(f"SELECT recipe: {recipe_}\n")

        # show the links from this recipe to the tags
        if recipe_:
            for tag_link in recipe_.tag_links:
                lg.debug(f"recipe.tag_link: {tag_link}")

        # add a second recipe with the same tag
        recipe2 = Recipe(
            recipe_id=2,
            title="recipe2",
            author=author1,
        )
        recipe_tag_link3 = RecipeTagLink(
            recipe=recipe2,
            tag=tag1,
            confidence=0.7,
            origin="user",
        )
        session.add(recipe_tag_link3)
        session.commit()

        # show the links from a tag to all recipes with this tag
        query = select(Tag).where(Tag.id == tag1.id)
        tag_ = session.exec(query).first()
        if tag_:
            for recipe_link in tag_.recipe_links:
                lg.debug(f"tag.recipe_link: {recipe_link}")

        # show the recipe from the tag link
        if tag_ and len(tag_.recipe_links) > 0:
            tag_recipe_link_ = tag_.recipe_links[0]
            lg.debug(f"tag_recipe_link.recipe: {tag_recipe_link_.recipe}")

        # directly query the link table, filtering for high confidence
        query = (
            select(RecipeTagLink)
            .where(RecipeTagLink.tag_id == tag1.id)
            .where(RecipeTagLink.confidence > 0.8)
            .order_by(RecipeTagLink.confidence)
        )
        recipe_tag_links_ = session.exec(query).all()
        for recipe_tag_link_ in recipe_tag_links_:
            lg.debug(f"recipe_tag_link: {recipe_tag_link_}")


def main() -> None:
    """Create the database and tables, then create authors and recipes."""
    create_db_and_tables()
    create_author_recipe_tag()


if __name__ == "__main__":
    main()
