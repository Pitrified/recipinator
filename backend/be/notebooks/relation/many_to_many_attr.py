"""SQLModel many to many relationship using links in the main tables.

Use an explicit link table, that can hold additional information about the links.
"""

from pathlib import Path
import sqlite3

# from sqlalchemy import func
import sqlalchemy.exc

from sqlmodel import (
    Field,
    Relationship,
    Session,
    SQLModel,
    UniqueConstraint,
    col,
    func,
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


# class RecipeTagLinkRead(RecipeTagLink):
#     """Link recipes and tags, with valid foreign keys."""
#     recipe_id: int
#     tag_id: int


class Recipe(SQLModel, table=True):
    """A recipe is identified by a shortcode."""

    id: int | None = Field(primary_key=True, default=None)

    shortcode: int = Field(index=True, unique=True)
    title: str

    author_id: int | None = Field(foreign_key="author.id", default=None)
    author: Author = Relationship(back_populates="recipes")

    tag_links: list[RecipeTagLink] = Relationship(back_populates="recipe")


class Tag(SQLModel, table=True):
    """A tag is identified by its name."""

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
            shortcode=1,
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

        # find a recipe with an explicit primary key (id)
        query = select(Recipe).where(Recipe.id == recipe1.id)
        recipe_ = session.exec(query).first()
        lg.debug(f"SELECT recipe primary  : {recipe_}\n")

        # find a recipe with an implicit primary key (shortcode)
        query = select(Recipe).where(Recipe.shortcode == 1)
        recipe_ = session.exec(query).first()
        lg.debug(f"SELECT recipe shortcode: {recipe_}\n")

        # show the links from this recipe to the tags
        if recipe_:
            for tag_link in recipe_.tag_links:
                lg.debug(f"recipe.tag_link: {tag_link}")

        # add a second recipe with the same tag
        recipe2 = Recipe(
            shortcode=2,
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

        # add new tags and new recipes
        tag3 = Tag(name="tag3", description="description of tag3", usefulness=0.8)
        recipe3 = Recipe(shortcode=3, title="recipe3", author=author1)
        recipe_tag_link33 = RecipeTagLink(
            recipe=recipe3, tag=tag3, confidence=0.85, origin="user"
        )
        session.add(recipe_tag_link33)
        session.commit()

        # find all distinct recipes whose tags (name) are in a list of tags
        tag_name_list = ["tag1", "tag2"]
        query = (
            select(Recipe)
            .distinct()
            .join(RecipeTagLink)
            .join(Tag)
            .where(col(Tag.name).in_(tag_name_list))
        )
        recipe_tag_list = session.exec(query).all()
        for recipe_tag_ in recipe_tag_list:
            lg.debug(f"recipe_tag: {recipe_tag_}")

        # select the recipes with a tag name in a list of tag names
        # also select the tag name, usefulness, and link confidence
        query = (
            # select(Recipe, Tag.name, Tag.usefulness, RecipeTagLink.confidence)
            # select(Recipe, Tag.name, Tag.usefulness)
            select(Recipe, RecipeTagLink.confidence)
            .join(RecipeTagLink)
            .join(Tag)
            .where(col(Tag.name).in_(tag_name_list))
        )
        recipe_tag_list = session.exec(query).all()
        for recipe_tag_ in recipe_tag_list:
            lg.debug(f"recipe_tag: {recipe_tag_}")
            lg.debug(f"\trecipe: {recipe_tag_[0]}")
            lg.debug(f"\tconfidence: {recipe_tag_[1]}")

        # select the recipe tag links with a tag name in a list of tag names
        # also select the tag and the recipe
        # (note that you can select single fields as well as whole objects)
        query = (
            # select(RecipeTagLink, Tag, Recipe)
            # select(RecipeTagLink, Tag.usefulness, Recipe)
            select(RecipeTagLink.confidence, Tag.usefulness, Recipe)
            .join(Recipe)
            .join(Tag)
            .where(col(Tag.name).in_(tag_name_list))
        )
        recipe_tag_list = session.exec(query).all()
        for recipe_tag_ in recipe_tag_list:
            lg.debug(f"row                         : {recipe_tag_}")
            # lg.debug(f"\trecipe_tag_link: {recipe_tag_[0]}")
            lg.debug(f"  recipe_tag_link.confidence: {recipe_tag_[0]}")
            # lg.debug(f"\t            tag: {recipe_tag_[1]}")
            lg.debug(f"              tag.usefulness: {recipe_tag_[1]}")
            lg.debug(f"                      recipe: {recipe_tag_[2]}")
            # lg.debug(f"                      recipe: {recipe_tag_['Recipe']}")

        # what happens if a new recipe is added with a tag that already exists?
        tag1_bis = Tag(name="tag1")
        recipe4 = Recipe(shortcode=4, title="recipe4", author=author1)
        recipe_tag_link1b4 = RecipeTagLink(
            recipe=recipe4, tag=tag1_bis, confidence=0.95, origin="user"
        )
        session.add(recipe_tag_link1b4)
        try:
            session.commit()
        # the sqlite3.IntegrityError raises
        # sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError)
        except sqlalchemy.exc.IntegrityError as e:
            lg.debug(f"{e}")
            session.rollback()

        # select all tags and count the number of recipes with each tag
        # sort by the count
        query = (
            # select(Tag, func.count(RecipeTagLink.recipe_id))
            select(Tag, func.count(RecipeTagLink.recipe_id))
            # select(Tag.name, Tag.id, func.count())
            # select(Tag.name, func.count())
            # select(Tag, func.count(RecipeTagLinkRead.recipe_id))
            .join(RecipeTagLink).group_by(Tag.id)
            # .group_by(Tag.name)
            .order_by(func.count(RecipeTagLink.recipe_id).desc())
        )
        tag_count_list = session.exec(query).all()
        for tag_count_ in tag_count_list:
            lg.debug(f"tag_count: {tag_count_}")
            # lg.debug(f"tag_count: {tag_count_['name']}")

        # use a CTE to also compute a score for each tag
        # the score is the product of the usefulness and the count
        query_cte = (
            select(Tag, func.count(RecipeTagLink.recipe_id).label("recipe_count"))
            # select(Tag, func.count(RecipeTagLink.recipe_id))
            .join(RecipeTagLink).group_by(Tag)
        ).cte("tag_count")
        # query = select(query_cte, query_cte.c.count * Tag.usefulness).order_by(
        #     query_cte.c.count * Tag.usefulness
        # )
        query = select(
            query_cte,
            # query_cte.c.recipe_count,
            # query_cte.c.count * query_cte.c.usefulness,
            (query_cte.c.recipe_count * query_cte.c.usefulness).label("score"),
        ).order_by(query_cte.c.recipe_count * query_cte.c.usefulness)
        tag_count_list = session.exec(query).all()
        for tag_count_ in tag_count_list:
            lg.debug(f"tag_count: {tag_count_}")
            lg.debug(f"         : {tag_count_['name']} {tag_count_['score']}")


def main() -> None:
    """Create the database and tables, then create authors and recipes."""
    create_db_and_tables()
    create_author_recipe_tag()


if __name__ == "__main__":
    main()
