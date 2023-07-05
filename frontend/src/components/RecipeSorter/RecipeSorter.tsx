import React, { useState, useEffect } from "react";
import RecipeCard from "../RecipeCard/RecipeCard";

import { DragDropContext, Draggable } from "react-beautiful-dnd";
import StrictModeDroppable from "../StrictModeDroppable/StrictModeDroppable";

const RecipeSorter = ({
  recipes,
  handleDragEnd,
  setRecipes
}) => {
  //   return (
  //     <div className="recipe-sorter-container">
  //       <h1>Recipe Sorter</h1>
  //       {recipes.map((recipe) => (
  //         <RecipeCard key={recipe.shortcode} recipe={recipe} />
  //       ))}
  //     </div>
  //   );

  const onDragEnd = (result) => {
    console.log('           begin: ', new Date().getTime());
    console.log(result);

    // not dropped in a valid location
    if (!result.destination) return;

    console.log(
      "moving from",
      result.source.index,
      "to",
      result.destination.index
    );

    // the droppableId is the whole list we are moving
    // console.log("moving from", result.source.droppableId);
    // console.log("moving to", result.destination.droppableId);

    // print info on draggableId
    console.log("draggableId", result.draggableId);

    // use the index to get the recipes in the array
    const clickedRecipe = recipes[result.source.index];
    const replacedRecipe = recipes[result.destination.index];
    console.log("clickedRecipe", clickedRecipe.shortcode);
    console.log("replacedRecipe", replacedRecipe.shortcode);

    console.log('pre front update: ', new Date().getTime());
    // we also update the frontend immediately
    // then we tell the backend to update the database
    const updatedRecipes = Array.from(recipes);
    const [reorderedRecipe] = updatedRecipes.splice(result.source.index, 1);
    updatedRecipes.splice(result.destination.index, 0, reorderedRecipe);
    setRecipes(updatedRecipes);

    // extract the shortcodes and send those to the RecipeBrowser
    console.log('pre back  update: ', new Date().getTime());
    handleDragEnd(clickedRecipe.shortcode, replacedRecipe.shortcode);
    console.log('post back update: ', new Date().getTime());
  };

  return (
    <div className="recipe-sorter-container">
      <h1>Recipe Sorter</h1>
      <DragDropContext onDragEnd={onDragEnd}>
        <div>
          <StrictModeDroppable droppableId="recipe-sorter-droppable">
            {(provided) => (
              <div
                {...provided.droppableProps}
                ref={provided.innerRef}
                className="recipe-sorter-list"
              >
                {recipes.map((recipe, idx) => (
                  <Draggable
                    key={recipe.shortcode}
                    draggableId={recipe.shortcode}
                    index={idx}
                  >
                    {(provided) => (
                      <div
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                        ref={provided.innerRef}
                      >
                        <RecipeCard recipe={recipe} />
                      </div>
                    )}
                  </Draggable>
                ))}
                {provided.placeholder}
              </div>
            )}
          </StrictModeDroppable>
        </div>
      </DragDropContext>
    </div>
  );
};

export default RecipeSorter;
