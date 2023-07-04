import React, { useState, useEffect } from "react";
import RecipeCard from "../RecipeCard/RecipeCard";

import { DragDropContext, Draggable } from "react-beautiful-dnd";
import StrictModeDroppable from "../StrictModeDroppable/StrictModeDroppable";

const RecipeSorter = ({ recipes, handleDragEnd }) => {
  //   return (
  //     <div className="recipe-sorter-container">
  //       <h1>Recipe Sorter</h1>
  //       {recipes.map((recipe) => (
  //         <RecipeCard key={recipe.shortcode} recipe={recipe} />
  //       ))}
  //     </div>
  //   );

  const onDragEnd = (result) => {
    console.log(result);
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

    // extract the shortcodes and send those to the RecipeBrowser
    // handleDragEnd(result);
  };

  return (
    <div className="recipe-sorter-container">
      <h1>Recipe Sorter</h1>
      <DragDropContext onDragEnd={onDragEnd}>
        <div>
          <StrictModeDroppable droppableId="recipe-sorter-droppable">
            {(provided) => (
              <ol
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
                      <li
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                        ref={provided.innerRef}
                      >
                        <RecipeCard recipe={recipe} />
                      </li>
                    )}
                  </Draggable>
                ))}
                {provided.placeholder}
              </ol>
            )}
          </StrictModeDroppable>
        </div>
      </DragDropContext>
    </div>
  );
};

export default RecipeSorter;
