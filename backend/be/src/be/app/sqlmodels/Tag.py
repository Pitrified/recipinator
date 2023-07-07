"""Possible tags for recipes."""

from sqlmodel import Field, SQLModel


class TagBase(SQLModel):
    """A tag for a recipe."""

    name: str = Field(primary_key=True)

    usefulness: int = Field(default=0)


class Tag(TagBase, table=True):
    """A tag for a recipe."""
