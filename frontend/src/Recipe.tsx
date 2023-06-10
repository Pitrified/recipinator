import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Recipe.css";

const api_url = "http://127.0.0.1:8000";

const Step = ({ id, text, handleAddStepAfter }) => {
  return (
    <li className="step-item">
      <span className="step-number">Step {id}:</span>
      <div className="step-text">{text}</div>
      <button onClick={handleAddStepAfter}>+</button>
    </li>
  );
};

const Preparation = ({ id, name, steps, addStep }) => {
  const [newStepText, setNewStepText] = useState("");
  const [selectedStepId, setSelectedStepId] = useState(
    steps[steps.length - 1]?.id
  );

  const handleAddStepAfter = () => {
    if (newStepText !== "" && selectedStepId !== null) {
      addStep(id, selectedStepId, newStepText);
      setNewStepText("");
      setSelectedStepId(null);
    }
  };

  const moveInputAfterSelectedStep = () => {
    return steps.map((step) => (
      <React.Fragment key={step.id}>
        <Step
          id={step.id}
          text={step.text}
          handleAddStepAfter={() => setSelectedStepId(step.id)}
        />
        {selectedStepId === step.id && (
          <div>
            <input
              type="text"
              className="step-text"
              value={newStepText}
              onChange={(e) => setNewStepText(e.target.value)}
            />
            <button className="add-step-button" onClick={handleAddStepAfter}>
              Add Step
            </button>
          </div>
        )}
      </React.Fragment>
    ));
  };

  return (
    <div>
      <h2>{name}</h2>
      <ol className="step-list">{moveInputAfterSelectedStep()}</ol>
    </div>
  );
};

const Recipe = () => {
  const [recipeData, setRecipeData] = useState(null);

  useEffect(() => {
    fetchRecipeData();
  }, []);

  const fetchRecipeData = async () => {
    try {
      const response = await axios.get(`${api_url}/api/recipe`);
      setRecipeData(response.data);
    } catch (error) {
      console.error("Error fetching recipe data:", error);
    }
  };

  const saveRecipeData = async (updatedRecipeData) => {
    try {
      await axios.put(api_url + "/api/recipe", updatedRecipeData);
    } catch (error) {
      console.error("Error saving recipe data:", error);
    }
  };

  const addStep = async (preparationId, stepId, stepText) => {
    try {
      await axios.post(`${api_url}/api/preparation/${preparationId}/steps`, {
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
    <div>
      <h1>{recipeData.title}</h1>
      {recipeData.preparations.map((preparation) => (
        <Preparation
          key={preparation.id}
          id={preparation.id}
          name={preparation.name}
          steps={preparation.steps}
          addStep={addStep}
        />
      ))}
    </div>
  );
};

export default Recipe;
