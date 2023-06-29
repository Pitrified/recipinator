"""CRUD operations for the app."""

from be.app.sqlmodels.Recipe import Recipe, RecipeRead
from loguru import logger as lg
from sqlmodel import Session, select

from be.app.sqlmodels.Author import Author, AuthorCreate, AuthorRead
from be.social.insta.structures import PostIg, ProfileIg


def create_author_from_profile(
    session: Session,
    profile: ProfileIg,
) -> AuthorRead:
    """Create an Author from a ProfileIg.

    Avoid creating duplicates.
    """
    # try to load an existing author with matching userid and username
    author_res = session.get(Author, (profile.username, profile.userid))
    if author_res:
        lg.debug(f"found existing author {author_res=}")
        author_read = AuthorRead.from_orm(author_res)
        return author_read

    # create a new author
    # MAYBE a profile.to_author() method?
    author_create = AuthorCreate(
        username=profile.username,
        userid=profile.userid,
        full_name=profile.full_name,
        biography=profile.biography,
    )
    lg.debug(f"built {author_create=}")
    author = Author.from_orm(author_create)
    session.add(author)
    session.commit()
    session.refresh(author)
    author_read = AuthorRead.from_orm(author)
    lg.debug(f"  got {author_read=}")

    return author_read


def create_recipe_from_post(
    session: Session,
    post: PostIg,
    author_read: AuthorRead,
) -> RecipeRead:
    """Create a Recipe from a PostIg.

    Avoid creating duplicates.
    """
    # try to load an existing recipe with matching shortcode
    # recipe_res = session.get(Recipe, post.shortcode)
    # if recipe_res:
    #     lg.debug(f"found existing recipe {recipe_res=}")
    #     recipe_read = RecipeRead.from_orm(recipe_res)
    #     return recipe_read
    recipe_read = get_recipe_from_shortcode(session, post.shortcode)
    if recipe_read:
        return recipe_read

    # create a new recipe
    # MAYBE a post.to_recipe() method?
    # recipe = RecipeCreate(
    recipe = Recipe(
        title=post.caption[:100],
        shortcode=post.shortcode,
        caption_original=post.caption,
        caption_clean=post.caption,
        has_url_media=post.has_url_media,
        has_video_url_media=post.has_video_url_media,
        author_userid=author_read.userid,
        author_username=author_read.username,
        # author=author,
        # author=author_create,
    )
    lg.debug(f"built {recipe=}")
    # add the recipe to the database
    # recipe = Recipe.from_orm(recipe)
    # recipe.author = Author.from_orm(author_read)
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    lg.debug(f"  got {recipe=}")
    # return_recipe = RecipeReadWithAuthor.from_orm(recipe)
    recipe_read = RecipeRead.from_orm(recipe)
    return recipe_read


def get_recipe_from_shortcode(session: Session, shortcode: str) -> RecipeRead | None:
    """Get a recipe from the database."""
    recipe_res = session.get(Recipe, shortcode)
    if recipe_res:
        lg.debug(f"found existing recipe {recipe_res=}")
        recipe_read = RecipeRead.from_orm(recipe_res)
        return recipe_read
    lg.debug(f"recipe {shortcode=} not found")
    return None


def get_all_recipes(
    session: Session,
    offset: int = 0,
    limit: int = 100,
) -> list[RecipeRead]:
    """Get all recipes from the database.

    FIXME: the key difference from tiangolo's code is that we specify the return type
           while he uses a response_model in the route.
           https://sqlmodel.tiangolo.com/tutorial/fastapi/limit-and-offset/#add-a-limit-and-offset-to-the-query-parameters
           so we cast the results to RecipeRead explicitly to type check,
           but I think that it is redundant.
           Except that this function does return RecipeRead, so it does make sense.
    """
    recipes = session.exec(select(Recipe).offset(offset).limit(limit)).all()
    lg.debug(f"got {len(recipes)=}")
    return [RecipeRead.from_orm(recipe) for recipe in recipes]


def get_number_of_recipes(session: Session) -> int:
    """Get the number of recipes in the database."""
    rows = session.query(Recipe.shortcode).count()
    return rows
