"""Shuffle recipes in the database."""

from sqlmodel import SQLModel


class RecipeShuffle(SQLModel):
    """Shuffle recipes in the database."""

    shortcodeClicked: str
    shortcodeReplaced: str
    shuffle_type: str
