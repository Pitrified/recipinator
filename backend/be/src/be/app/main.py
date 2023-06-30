"""App for the backend service."""

from be.app.crud import (
    create_author_from_profile,
    create_recipe_from_post,
    get_all_recipes,
    get_recipe_from_shortcode,
)
from be.app.database import create_db_and_tables, get_session
from be.app.sqlmodels.Author import Author, AuthorCreate, AuthorRead
from be.app.sqlmodels.Recipe import Recipe, RecipeCreate, RecipeRead
from be.social.insta.loader import InstaLoader
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session
from fastapi.middleware.cors import CORSMiddleware

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

# Enable CORS (Cross-Origin Resource Sharing) to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this list with the appropriate frontend URL(s)
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


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

    author_read = create_author_from_profile(session, pf)

    recipe_read = create_recipe_from_post(session, ps, author_read)

    return recipe_read


@app.get("/recipes/", response_model=list[RecipeRead])
def read_recipes(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
) -> list[RecipeRead]:
    """Load all recipes with pagination."""
    recipes = get_all_recipes(session=session, offset=offset, limit=limit)
    return recipes
