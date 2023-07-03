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
                {recipes.map((recipe) => (
                  <Draggable
                    key={recipe.shortcode}
                    draggableId={recipe.shortcode}
                    index={0} // FIXME the drag works badly probably needs this ops
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
