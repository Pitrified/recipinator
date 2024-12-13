# """Pydantic schemas for the API."""


# from typing import List
# from pydantic import BaseModel


# class SimpleRecipe(BaseModel):
#     """A simple recipe."""

#     recipe_id: int
#     title: str
#     caption_original: str
#     caption_clean: str
#     has_url_media: bool
#     has_video_url_media: bool


# class RecipeAuthor(BaseModel):
#     """Link a recipe to an author.

#     To learn more, we could use the back_populates parameter,
#     and have a 1vN relationship between Recipe and Author,
#     skipping the RecipeAuthor table.

#     We will learn about NvN relationships in RecipeTags.
#     """

#     recipe_id: int
#     author_id: int


# class Author(BaseModel):
#     """An author of a recipe."""

#     author_id: int
#     name: str
#     page_link: str


# class RecipeTags(BaseModel):
#     """The tags of a recipe."""

#     recipe_id: int
#     tag_id: int


# class Tag(BaseModel):
#     """A tag."""

#     tag_id: int
#     name: str
