"""Recipe models."""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

if TYPE_CHECKING:
    from .Author import Author, AuthorRead


class RecipeBase(SQLModel):
    """Base recipe model."""

    title: str
    caption_original: str
    caption_clean: str
    has_url_media: bool
    has_video_url_media: bool

    author_id: int = Field(foreign_key="author.id")


class Recipe(RecipeBase, table=True):
    """A simple recipe.

    This is a SQLModel table.
    """

    id: int | None = Field(default=None, primary_key=True)

    author: "Author" = Relationship(back_populates="recipes")


class RecipeCreate(RecipeBase):
    """Create a recipe."""

    # pass
    author: "Author"
    # author: "Author" = Relationship(back_populates="recipes")


class RecipeRead(RecipeBase):
    """Read a recipe."""

    id: int

    # author: "Author" # ? AuthorRead is in RecipeReadWithAuthor


class RecipeUpdate(RecipeBase):
    """Update a recipe."""

    title: str | None = None
    caption_original: str | None = None
    caption_clean: str | None = None
    has_url_media: bool | None = None
    has_video_url_media: bool | None = None

    author_id: int | None = None


class RecipeReadWithAuthor(RecipeRead):
    """Read a recipe with its author."""

    author: "AuthorRead"
