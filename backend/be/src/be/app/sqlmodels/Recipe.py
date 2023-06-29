"""Recipe models."""

from typing import TYPE_CHECKING
from be.app.sqlmodels.Author import AuthorCreate

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

if TYPE_CHECKING:
    from .Author import Author, AuthorRead


class RecipeBase(SQLModel):
    """Base recipe model."""

    title: str
    shortcode: str = Field(primary_key=True)
    caption_original: str
    caption_clean: str
    has_url_media: bool
    has_video_url_media: bool

    def __repr__(self) -> str:
        """Return a string representation of a Recipe."""
        title_clean = self.title.replace("\n", " ")
        return (
            f"{self.__class__.__name__}({self.shortcode}"
            f" : {title_clean}"
            # f" : {self.caption_original[:100]}"
            ")"
        )

    def __str__(self) -> str:
        """Return a string representation of a Recipe."""
        return self.__repr__()


class Recipe(RecipeBase, table=True):
    """A simple recipe.

    This is a SQLModel table.
    """

    # id: int | None = Field(default=None, primary_key=True)

    author_userid: int = Field(foreign_key="author.userid")
    author_username: str = Field(foreign_key="author.username")

    # Relationships are a smart idea to do less queries but I can't set two foreign keys
    # let's learn one step at a time
    # # author: "Author" = Relationship(back_populates="recipes")
    # author: "Author" = Relationship(
    #     back_populates="recipes",
    #     sa_relationship_kwargs={
    #         "foreign_keys": [
    #             author_userid,
    #             author_username,
    #         ]
    #     },
    # )
    # # sa_relationship_kwargs={ 'foreign_keys': [updated_by_id] }


class RecipeCreate(RecipeBase):
    """Create a recipe."""

    # pass
    # I don't know if this is needed
    # I just pass the primary keys of the author :'(
    # author: "Author"
    # author: "Author" = Relationship(back_populates="recipes")


class RecipeRead(RecipeBase):
    """Read a recipe."""

    # id: int

    # author: "Author" # ? AuthorRead is in RecipeReadWithAuthor


class RecipeUpdate(RecipeBase):
    """Update a recipe."""

    title: str | None = None
    caption_original: str | None = None
    caption_clean: str | None = None
    has_url_media: bool | None = None
    has_video_url_media: bool | None = None

    # author_id: int | None = None


class RecipeReadWithAuthor(RecipeRead):
    """Read a recipe with its author."""

    author: "AuthorRead"
