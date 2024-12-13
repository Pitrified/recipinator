# """SQLAlchemy models for the backend."""

# from be.app.database import Base

# from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
# from sqlalchemy.orm import relationship


# class SimpleRecipe(Base):
#     """A simple recipe."""

#     __tablename__ = "simple_recipe"

#     recipe_id = Column(Integer, primary_key=True)
#     title = Column(String)
#     caption_original = Column(String)
#     caption_clean = Column(String)
#     has_url_media = Column(Boolean)
#     has_video_url_media = Column(Boolean)


# class RecipeAuthor(Base):
#     """Link a recipe to an author."""

#     __tablename__ = "recipe_authors"

#     recipe_id = Column(Integer, ForeignKey("simple_recipe.recipe_id"), primary_key=True)
#     author_id = Column(Integer, ForeignKey("author.author_id"), primary_key=True)


# class Author(Base):
#     """An author of a recipe."""

#     __tablename__ = "author"

#     author_id = Column(Integer, primary_key=True)
#     name = Column(String)
#     link = Column(String)


# class RecipeTags(Base):
#     """The tags of a recipe."""

#     __tablename__ = "recipe_tags"

#     recipe_id = Column(Integer, ForeignKey("simple_recipe.recipe_id"), primary_key=True)
#     tag_id = Column(Integer, ForeignKey("tag.tag_id"), primary_key=True)


# class Tag(Base):
#     """A tag."""

#     __tablename__ = "tag"

#     tag_id = Column(Integer, primary_key=True)
#     name = Column(String)
