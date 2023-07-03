import React, { useState, useEffect } from "react";
import axios from "axios";

import { API_URL } from "../../config";

import "./RecipeList.css";

// minimal recipe data shower
const RecipeCard = ({ recipe }) => {
  return (
    <div className="recipe-card">
      <h2 className="recipe-name">{recipe.title}</h2>
    </div>
  );
};


const RecipeList = () => {
  const [recipeData, setRecipeData] = useState<any[]>([]);

  useEffect(() => {
    fetchRecipeData();
  }, []);

  const fetchRecipeData = async () => {
    try {
      const response = await axios.get(`${API_URL}/recipes`);
      console.log("response.data:", response.data);
      setRecipeData(response.data);
    } catch (error) {
      console.error("Error fetching recipe data:", error);
    }
  };

  // check for the length of the array
  if (recipeData.length === 0) {
    return <div>Loading...</div>;
  }

  return (
    <div className="recipe-list-container">
      {recipeData.map((recipe) => (
        <RecipeCard key={recipe.shortcode} recipe={recipe} />
      ))}
    </div>
  );
};

export default RecipeList;