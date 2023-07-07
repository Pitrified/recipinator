"""Test one to many relationship using two foreign keys and proper inheritance."""

from typing import Any, Generator
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import (
    Field,
    ForeignKeyConstraint,
    Relationship,
    SQLModel,
    Session,
    create_engine,
    select,
)


class AuthorBase(SQLModel):
    """An author is identified by a userid and a username."""

    userid: int = Field(primary_key=True)
    username: str = Field(primary_key=True)

    age: int | None = Field(default=None, nullable=True)


class Author(AuthorBase, table=True):
    """An author in the database."""

    recipes: list["Recipe"] = Relationship(back_populates="author")


class AuthorCreate(AuthorBase):
    """To create an author, we do not need additional information."""


class AuthorRead(AuthorBase):
    """When reading an author, we do not get additional information."""


class AuthorUpdate(SQLModel):
    """Update an author's information."""

    # the primary key is also optional because we do not need it to update an author
    # in the app.patch call we have it as a parameter to select which author to update
    # then in author_update we have the info to update
    userid: int | None = None
    username: str | None = None
    age: int | None = None


class RecipeBase(SQLModel):
    """A recipe is identified by a recipeid."""

    recipeid: int = Field(primary_key=True)
    title: str

    author_userid: int | None = Field(default=None)
    author_username: str | None = Field(default=None)


class Recipe(RecipeBase, table=True):
    """A recipe in the database."""

    author: Author = Relationship(back_populates="recipes")

    __table_args__ = (
        ForeignKeyConstraint(
            ["author_userid", "author_username"],
            ["author.userid", "author.username"],
        ),
    )


class RecipeCreate(Recipe):
    """To create a recipe, we do not need additional information."""


class RecipeRead(RecipeBase):
    """When reading a recipe, we do not get additional information."""


class RecipeUpdate(SQLModel):
    """Update a recipe's information."""

    recipeid: int | None = None
    title: str | None = None
    author_userid: int | None = None
    author_username: str | None = None


class AuthorReadWithRecipes(AuthorRead):
    """When reading an author, we get additional information."""

    recipes: list[RecipeRead] = []


class RecipeReadWithAuthor(RecipeRead):
    """When reading a recipe, we get additional information."""

    author: AuthorRead | None = None


sqlite_file_name = "local_o2m_with.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables() -> None:
    """Create the database and tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, Any, None]:
    """Get a session."""
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    """Run on startup."""
    create_db_and_tables()


@app.post("/authors/", response_model=AuthorRead)
def create_author(*, session: Session = Depends(get_session), author: AuthorCreate):
    """Create an author."""
    db_author = Author.from_orm(author)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author


@app.get("/authors/", response_model=list[AuthorRead])
def read_authors(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    """Read authors with offset and limit."""
    authors = session.exec(select(Author).offset(offset).limit(limit)).all()
    return authors


@app.get("/author_with_recipe/", response_model=AuthorReadWithRecipes)
def read_author(
    *,
    session: Session = Depends(get_session),
    author_id: int,
    author_username: str,
):
    """Read an author with recipes."""
    author = session.get(Author, (author_id, author_username))
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/recipes/", response_model=RecipeRead)
def create_recipe(
    *,
    session: Session = Depends(get_session),
    recipe: RecipeCreate,
) -> RecipeRead:
    """Create a recipe."""
    db_recipe = Recipe.from_orm(recipe)
    session.add(db_recipe)
    session.commit()
    session.refresh(db_recipe)
    # return db_recipe
    # which is better? this is clearer but the FastAPI already serializes it
    return RecipeRead.from_orm(db_recipe)


@app.get("/recipe_with_author/", response_model=RecipeReadWithAuthor)
def read_recipe(
    *,
    session: Session = Depends(get_session),
    recipe_id: int,
):
    """Read a recipe with author."""
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


def populate_db() -> None:
    """Populate the database with some data."""
    import requests

    url = "http://localhost:8000/"

    # create the first one manually
    author1 = AuthorCreate(userid=1, username="author1", age=20)
    r = requests.post(url + "authors/", json=author1.dict())
    print(r.json())

    # create a recipe for author1, who already exists
    recipe1 = RecipeCreate(
        recipeid=1,
        title="recipe1",
        author=Author.from_orm(author1),
    )
    r = requests.post(url + "recipes/", json=recipe1.dict())
    print(r.json())

    # the second author will be created directly from the recipe
    author2 = AuthorCreate(userid=2, username="author2", age=30)
    recipe2 = RecipeCreate(
        recipeid=2,
        title="recipe2",
        author=Author.from_orm(author2),
    )
    r = requests.post(url + "recipes/", json=recipe2.dict())
    print(r.json())


if __name__ == "__main__":
    populate_db()
