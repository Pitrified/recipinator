import React from "react";

const RecipeCard = ({ recipe }) => {

  const shortTitle = (title: string) => { 
    if (title.length > 20) {
      return title.substring(0, 4) + "...";
    } else {
      return title;
    }
  };

  return (
    <div className="recipe-card">
      {/* <h2 className="recipe-name">{recipe.title}</h2> */}
      <h2 className="recipe-name">{shortTitle(recipe.title)}</h2>
    </div>
  );
};

export default RecipeCard;
