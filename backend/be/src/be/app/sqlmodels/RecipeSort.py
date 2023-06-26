"""A kinda linked list of recipes.

A recipe can only have one previous recipe, and can only appear once.
The first recipe has no previous recipe.
To select the next recipe, select the recipe with the previous recipe id
equal to the current recipe id.
"""

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


class RecipeSortBase(SQLModel):
    """Base recipe sort model."""

    recipe_id: int = Field(foreign_key="recipe.id", primary_key=True)
    prev_recipe_id: int | None = Field(foreign_key="recipe.id", nullable=True)
    # next_recipe_id: int | None = Field(foreign_key="recipe.id", nullable=True)


class RecipeSort(RecipeSortBase, table=True):
    """A simple recipe sort.

    This is a SQLModel table.
    """
