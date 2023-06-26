"""App for the backend service."""

from be.app.database import create_db_and_tables, get_session
from be.app.sqlmodels.Author import Author, AuthorCreate, AuthorRead
from be.app.sqlmodels.Recipe import Recipe, RecipeCreate, RecipeRead
from be.social.insta.loader import InstaLoader
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session

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
) -> RecipeReadWithAuthor:
    """Create a recipe."""
    # load the post from the shortcode
    ps = il.load_post(shortcode)
    pf = il.load_profile(ps.profile)

    author_create = AuthorCreate(
        name=pf.username,
    )
    print(f"built {author_create=}")

    author = Author.from_orm(author_create)
    session.add(author)
    session.commit()
    session.refresh(author)
    author_read = AuthorRead.from_orm(author)
    print(f"  got {author_read=}")

    # MAYBE a ps.to_recipe() method?
    # recipe = RecipeCreate(
    recipe = Recipe(
        title=ps.caption,
        shortcode=ps.shortcode,
        caption_original=ps.caption,
        caption_clean=ps.caption,
        has_url_media=ps.has_url_media,
        has_video_url_media=ps.has_video_url_media,
        author_id=author_read.id,
        author=author,
        # author=author_create,
    )
    print(f"built {recipe=}")

    # add the recipe to the database
    # recipe = Recipe.from_orm(recipe)
    # recipe.author = Author.from_orm(author_read)
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    print(f"  got {recipe=}")
    return_recipe = RecipeReadWithAuthor.from_orm(recipe)
    return return_recipe
