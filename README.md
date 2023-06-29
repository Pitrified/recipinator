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

Python backend:

```bash
# workon py311
# pip install fastapi
# pip install "uvicorn[standard]"
poetry install
cd backend/be/src/be/app/
uvicorn main:app --reload
```

React frontend:

```
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
immediately,
then we can edit the recipe to add more info.

The steps/ingredients/time are deferred to a future edit page.

<!-- This is an enhanced version of the edit recipe page,
with more details to be ready for a copy paste. -->

#### Automatic info

We can generate the info automatically, then if needed edit it.
Yeah it's needed.

* Title? do instagram reels have a title?
* Image - just use the thumbnail

Python side:

1. from an id get the info
1. save the image, save the path to that in the class
1. save the video, save the path to that in the class
1. if we receive some text description save it
1. dump the class in a json file
1. shove the PostIg into the database
1. show the edit page for the recipe

While editing, the title is an input, the description is a textarea.
We have a list of tags, we can add new tags (with proposed tags), we can remove tags.
Every time we change something, we update the database and reload the recipe.

This is a `VagueRecipe`.
There will be a button to convert it to a `Recipe`,
where we can add the ingredients, the steps, the time in a more formal way.
Possibly in an automated way.

#### Manual info

The title?
Minimal tags.
Some notes to the recipe (simple list of text).

Then we can have a button to convert to standard recipe.

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

## Data model for minimal recipe

### SimpleRecipe

* RecipeID
* Title
* CaptionOriginal
* CaptionClean
* HasUrlMedia
* HasVideoUrlMedia

### RecipeAuthor

Multiple authors for a recipe.
Not really for a simple recipe, but we can have it.

* RecipeID
* AuthorID

### Author

* AuthorID
* Name
* Link to page

### RecipeTags

Multiple tags for a recipe.

* RecipeID
* TagID

### Tag

* TagID
* Name

Then we can have all the fancy tag similarity stuff to filter on them.

## Data model for full recipe

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

### Graph of recipes

We can have a graph of recipes, with edges between similar recipes.
Embedding of recipes, then we can have a graph of recipes.
Zoom in and out, click on a recipe to see it, hover to see the preview.
