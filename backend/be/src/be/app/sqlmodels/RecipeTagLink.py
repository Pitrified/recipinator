"""Link table between recipes and tags."""

from sqlmodel import Field, SQLModel


class RecipeTagLink(SQLModel, table=True):
    """Link table between recipes and tags."""

    recipe_shortcode: int = Field(foreign_key="recipe.shortcode", primary_key=True)
    tag_name: str = Field(foreign_key="tag.name", primary_key=True)

    confidence: float
    origin: str
