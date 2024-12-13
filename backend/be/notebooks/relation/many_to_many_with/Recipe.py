"""Many to Many Recipe."""

from typing import TYPE_CHECKING
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

if TYPE_CHECKING:
    from .Author import Author, AuthorRead


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
