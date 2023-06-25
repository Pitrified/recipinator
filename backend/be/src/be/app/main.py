"""App for the backend service."""

from be.app.database import create_db_and_tables, get_session
from be.app.sqlmodels.Author import Author, AuthorRead
from be.app.sqlmodels.Recipe import Recipe, RecipeCreate, RecipeRead
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session

# from be.app.sqlmodels.Recipe import RecipeReadWithAuthor
# RecipeReadWithAuthor.update_forward_refs()
# # with update:    NameError: name 'AuthorRead' is not defined
# # without update: TypeError: issubclass() arg 1 must be a class


app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    """Create the database and tables on startup."""
    create_db_and_tables()


# @app.get("/recipe_author/{recipe_id}", response_model=RecipeReadWithAuthor)
# def read_recipe_author(*, session: Session = Depends(get_session), recipe_id: int):
#     """Read a recipe."""
#     recipe = session.get(Recipe, recipe_id)
#     if not recipe:
#         raise HTTPException(status_code=404, detail="Recipe not found")
#     return recipe


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
) -> RecipeRead:
    """Create a recipe."""
    print(f"got    {type(recipe)=}")
    db_recipe = Recipe.from_orm(recipe)
    print(f"    {type(db_recipe)=}")
    session.add(db_recipe)
    session.commit()
    session.refresh(db_recipe)
    return_recipe = RecipeRead.from_orm(db_recipe)
    # return db_recipe
    return return_recipe
