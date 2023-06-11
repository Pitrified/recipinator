# Build a recipe site, a recipinator if you will

## Dev env

### Setup

* https://github.com/nvm-sh/nvm#installing-and-updating
* https://linuxize.com/post/how-to-install-node-js-on-ubuntu-22-04/
* https://www.freecodecamp.org/news/how-to-build-a-react-app-different-ways/#what-is-vite

Install nvm and node:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
nvm -v
nvm list-remote
nvm install node
node -v
```

Install dependencies:

```bash
npm install
```

### Run

```bash
# python backend
workon py311
pip install fastapi
pip install "uvicorn[standard]"
cd backend/
uvicorn main:app --reload

# react frontend
cd frontend/
npm run dev
```

## Flow of the app

### Home

Little more than a placeholder to go to add new recipe or browse recipes.

### Add a new recipe

Load info from social media
We have some instagram python API.

1. Title
1. Image:
    - from the video load a bunch of screenshot and pick one
    - use the thumbnail
    - load the whole video and pick a frame with a slider
1. Description:
    1. Ingredients
    1. Steps
    1. Tags
    1. Time
    1. A mystical embedding for recipe similarity
    1. A recipe can have sub preparation, should those be recipes?
       Like a besciamella is a recipe, but it's also a step in a lasagna recipe.
       There should be a way to link them, but also customize the sub recipe?

We shove all this info into the data model,
then we can edit the recipe to add more info.

This is an enhanced version of the edit recipe page,
with more details to be ready for a copy paste.

### Browse recipe

Search by title, ingredients, tags, time.
All the filters can be combined with AND and OR nested as needed.

A sexy tag selector with a cloud of tags and a graph and a search bar and some drag and drop.

While searching, show the recipes in a grid with the image and title.

While searching by ingredients, consider the substitutions.

### Show a recipe

Show the title, the image, the description, the ingredients, the steps, the tags, the time.

### Edit a recipe

There is a button to edit the recipe, it opens a new page with the form to edit the recipe.

### Similar recipes

Show similar recipes, manually set and based on the mystical embedding.

## Data model

### Recipe

* RecipeID
* Title
* Not here: Images
* Not here: Preparations
* Time
* Not here: Tags
* Serves
* Serve unit

### RecipeAuthor

Multiple authors for a recipe.

* RecipeID
* AuthorID

### D_Author

* AuthorID
* Name
* Link to page

### RecipeInspiration

* RecipeID
* Link to source
* Notes

### Preparation

Multiple preparation for a recipe.

* RecipeID
* PrepID
* Prep order
* Title
* Not here: Images
* Not here: Steps
* Time

### Step

Multiple steps for a preparation.

* PrepID
* StepID
* Step order
* Text
* Images

### PrepIngredient

* PrepID
* IngredientID
* Quantity

### D_Ingredient

* IngredientID
* Name
* Unit

## Ideas
 
The serve stat could be dynamic, like a slider that changes the quantities of the ingredients.
