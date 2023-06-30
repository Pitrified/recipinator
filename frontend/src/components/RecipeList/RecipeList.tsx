import React, { useState, useEffect } from "react";
import axios from "axios";

import { API_URL } from "../../config";

import RecipeCard from "../RecipeCard/RecipeCard";

import "./RecipeList.css";

const RecipeList = () => {
  const [recipeData, setRecipeData] = useState(null);

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

  if (!recipeData) {
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