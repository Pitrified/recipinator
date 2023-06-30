import React from "react";

const RecipeCard = ({ recipe }) => {
  return (
    <div className="recipe-card">
      <h2 className="recipe-name">{recipe.title}</h2>
    </div>
  );
};

export default RecipeCard;
