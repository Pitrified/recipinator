import React, { useState, useEffect } from "react";
import axios from "axios";

import { API_URL } from "../../config";

import Preparation from "../Preparation/Preparation";

import "./Recipe.css";

const Recipe = () => {
  const [recipeData, setRecipeData] = useState(null);

  useEffect(() => {
    fetchRecipeData();
  }, []);

  const fetchRecipeData = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/recipe`);
      setRecipeData(response.data);
    } catch (error) {
      console.error("Error fetching recipe data:", error);
    }
  };

  const saveRecipeData = async (updatedRecipeData) => {
    try {
      await axios.put(API_URL + "/api/recipe", updatedRecipeData);
    } catch (error) {
      console.error("Error saving recipe data:", error);
    }
  };

  const addStep = async (preparationId, stepId, stepText) => {
    try {
      await axios.post(`${API_URL}/api/preparation/${preparationId}/steps`, {
        id: stepId,
        text: stepText,
      });
      fetchRecipeData();
    } catch (error) {
      console.error("Error adding step:", error);
    }
  };

  if (!recipeData) {
    return <div>Loading...</div>;
  }

  return (
    <div className="recipe-container">
      <h1 className="recipe-name">{recipeData.title}</h1>
      {recipeData.preparations.map((preparation) => (
        <Preparation
          key={preparation.id}
          prep={preparation}
          addStep={addStep}
        />
      ))}
    </div>
  );
};

export default Recipe;