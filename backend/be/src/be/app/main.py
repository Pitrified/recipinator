"""App for the backend service."""

from be.app.database import create_db_and_tables, get_session
from be.app.sqlmodels.Author import Author, AuthorCreate, AuthorRead
from be.app.sqlmodels.Recipe import Recipe, RecipeCreate, RecipeRead
from be.social.insta.loader import InstaLoader
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session

from loguru import logger as lg

from be.app.sqlmodels.Recipe import RecipeReadWithAuthor

# RecipeReadWithAuthor.update_forward_refs()
# # with update:    NameError: name 'AuthorRead' is not defined
# # without update: TypeError: issubclass() arg 1 must be a class

# RecipeCreate.update_forward_refs()
RecipeCreate.update_forward_refs(Author=Author)
RecipeReadWithAuthor.update_forward_refs(AuthorRead=AuthorRead)


def get_il() -> InstaLoader:
    """Get an instance of InstaLoader.

    TODO: Proper login and save the state somehow.
    """
    il = InstaLoader("pynstachiooo")
    il.login()
    return il


app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    """Create the database and tables on startup."""
    create_db_and_tables()


@app.get("/recipe_author/{recipe_id}", response_model=RecipeReadWithAuthor)
def read_recipe_author(
    *,
    session: Session = Depends(get_session),
    recipe_id: int,
) -> Recipe:
    """Read a recipe, include Author information."""
    # is that a Recipe or a RecipeReadWithAuthor? Why do I need that?
    # Recipe has .author already
    recipe = session.get(Recipe, recipe_id)
    print(f"{recipe=}")
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    print(f"{recipe.caption_clean=}")
    print(f"{recipe.author=}")
    return recipe


@app.get("/recipe/{recipe_id}", response_model=RecipeRead)
def read_recipe(*, session: Session = Depends(get_session), recipe_id: int):
    """Read a recipe."""
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@app.post("/recipe/", response_model=RecipeRead)
def create_recipe(
    *,
    session: Session = Depends(get_session),
    recipe: RecipeCreate,
    # recipe: Recipe,
) -> RecipeRead:
    """Create a recipe."""
    print(f"{type(recipe)=}")
    print(f"{recipe=}")
    db_recipe = Recipe.from_orm(recipe)
    print(f"{type(db_recipe)=}")
    print(f"{db_recipe=}")
    # FIXME obviously this is not the right way to do this
    # db_recipe.author = Author.from_orm(recipe.author) ???
    # but really I want the from_orm to automatically populate .author
    # FAILS NOW :(
    author = Author.from_orm(recipe.author)
    db_recipe.author = author
    print(f"{db_recipe=}")
    session.add(db_recipe)
    session.commit()
    session.refresh(db_recipe)
    return_recipe = RecipeRead.from_orm(db_recipe)
    # return db_recipe
    return return_recipe


@app.post("/recipe_shortcode/")
def create_recipe_shortcode(
    *,
    session: Session = Depends(get_session),
    il: InstaLoader = Depends(get_il),
    shortcode: str,
    # ) -> RecipeReadWithAuthor:
) -> RecipeRead:
    """Create a recipe."""
    # load the post from the shortcode
    ps = il.load_post(shortcode)
    pf = il.load_profile(ps.profile)

    # try to load an existing author with matching userid and username
    author_res = session.get(Author, (pf.username, pf.userid))
    if author_res:
        lg.debug(f"found existing author {author_res=}")
        author_read = AuthorRead.from_orm(author_res)

    # create a new author
    else:
        author_create = AuthorCreate(
            username=pf.username,
            userid=pf.userid,
            full_name=pf.full_name,
            biography=pf.biography,
        )
        lg.debug(f"built {author_create=}")
        author = Author.from_orm(author_create)
        session.add(author)
        session.commit()
        session.refresh(author)
        author_read = AuthorRead.from_orm(author)
        lg.debug(f"  got {author_read=}")

    recipe_res = session.get(Recipe, ps.shortcode)
    if recipe_res:
        lg.debug(f"found existing recipe {recipe_res=}")
        return_recipe = RecipeRead.from_orm(recipe_res)

    # create a new recipe
    else:
        # MAYBE a ps.to_recipe() method?
        # recipe = RecipeCreate(
        recipe = Recipe(
            title=ps.caption[:100],
            shortcode=ps.shortcode,
            caption_original=ps.caption,
            caption_clean=ps.caption,
            has_url_media=ps.has_url_media,
            has_video_url_media=ps.has_video_url_media,
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
        return_recipe = RecipeRead.from_orm(recipe)

    return return_recipe
