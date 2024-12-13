"""Many to Many Author."""

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
    from .Recipe import Recipe, RecipeRead


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
