"""Author models."""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

if TYPE_CHECKING:
    from .Recipe import Recipe


class AuthorBase(SQLModel):
    """Base author model."""

    username: str = Field(primary_key=True)
    userid: int = Field(primary_key=True)
    full_name: str
    biography: str
    page_link: str | None = None


class Author(AuthorBase, table=True):
    """An author of a recipe.

    This is a SQLModel table.
    """

    # id: int | None = Field(default=None, primary_key=True)

    # recipes: list["Recipe"] = Relationship(back_populates="author")


class AuthorCreate(AuthorBase):
    """Create an author."""


class AuthorRead(AuthorBase):
    """Read an author."""

    # id: int


class AuthorUpdate(AuthorBase):
    """Update an author."""

    username: str
    userid: int
    full_name: str | None = None
    biography: str | None = None
    page_link: str | None = None
